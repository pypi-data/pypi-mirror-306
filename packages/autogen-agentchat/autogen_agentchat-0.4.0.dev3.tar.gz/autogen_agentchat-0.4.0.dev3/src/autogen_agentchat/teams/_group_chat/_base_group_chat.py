import asyncio
import uuid
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Callable, List

from autogen_core.application import SingleThreadedAgentRuntime
from autogen_core.base import (
    AgentId,
    AgentInstantiationContext,
    AgentRuntime,
    AgentType,
    CancellationToken,
    MessageContext,
    TopicId,
)
from autogen_core.components import ClosureAgent, TypeSubscription

from ...base import ChatAgent, TaskResult, Team, TerminationCondition
from ...messages import ChatMessage, InnerMessage, TextMessage
from .._events import GroupChatPublishEvent, GroupChatRequestPublishEvent
from ._base_group_chat_manager import BaseGroupChatManager
from ._chat_agent_container import ChatAgentContainer


class BaseGroupChat(Team, ABC):
    """The base class for group chat teams.

    To implement a group chat team, first create a subclass of :class:`BaseGroupChatManager` and then
    create a subclass of :class:`BaseGroupChat` that uses the group chat manager.
    """

    def __init__(
        self,
        participants: List[ChatAgent],
        group_chat_manager_class: type[BaseGroupChatManager],
        termination_condition: TerminationCondition | None = None,
    ):
        if len(participants) == 0:
            raise ValueError("At least one participant is required.")
        if len(participants) != len(set(participant.name for participant in participants)):
            raise ValueError("The participant names must be unique.")
        self._participants = participants
        self._team_id = str(uuid.uuid4())
        self._base_group_chat_manager_class = group_chat_manager_class
        self._termination_condition = termination_condition

    @abstractmethod
    def _create_group_chat_manager_factory(
        self,
        parent_topic_type: str,
        group_topic_type: str,
        participant_topic_types: List[str],
        participant_descriptions: List[str],
        termination_condition: TerminationCondition | None,
    ) -> Callable[[], BaseGroupChatManager]: ...

    def _create_participant_factory(
        self,
        parent_topic_type: str,
        output_topic_type: str,
        agent: ChatAgent,
    ) -> Callable[[], ChatAgentContainer]:
        def _factory() -> ChatAgentContainer:
            id = AgentInstantiationContext.current_agent_id()
            assert id == AgentId(type=agent.name, key=self._team_id)
            container = ChatAgentContainer(parent_topic_type, output_topic_type, agent)
            assert container.id == id
            return container

        return _factory

    async def run(
        self,
        task: str,
        *,
        cancellation_token: CancellationToken | None = None,
    ) -> TaskResult:
        """Run the team and return the result. The base implementation uses
        :meth:`run_stream` to run the team and then returns the final result."""
        async for message in self.run_stream(
            task,
            cancellation_token=cancellation_token,
        ):
            if isinstance(message, TaskResult):
                return message
        raise AssertionError("The stream should have returned the final result.")

    async def run_stream(
        self,
        task: str,
        *,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[InnerMessage | ChatMessage | TaskResult, None]:
        """Run the team and produces a stream of messages and the final result
        of the type :class:`TaskResult` as the last item in the stream."""
        # Create the runtime.
        runtime = SingleThreadedAgentRuntime()

        # Constants for the group chat manager.
        group_chat_manager_agent_type = AgentType("group_chat_manager")
        group_chat_manager_topic_type = group_chat_manager_agent_type.type
        group_topic_type = "round_robin_group_topic"
        team_topic_type = "team_topic"
        output_topic_type = "output_topic"

        # Register participants.
        participant_topic_types: List[str] = []
        participant_descriptions: List[str] = []
        for participant in self._participants:
            # Use the participant name as the agent type and topic type.
            agent_type = participant.name
            topic_type = participant.name
            # Register the participant factory.
            await ChatAgentContainer.register(
                runtime,
                type=agent_type,
                factory=self._create_participant_factory(group_topic_type, output_topic_type, participant),
            )
            # Add subscriptions for the participant.
            await runtime.add_subscription(TypeSubscription(topic_type=topic_type, agent_type=agent_type))
            await runtime.add_subscription(TypeSubscription(topic_type=group_topic_type, agent_type=agent_type))
            # Add the participant to the lists.
            participant_descriptions.append(participant.description)
            participant_topic_types.append(topic_type)

        # Register the group chat manager.
        await self._base_group_chat_manager_class.register(
            runtime,
            type=group_chat_manager_agent_type.type,
            factory=self._create_group_chat_manager_factory(
                parent_topic_type=team_topic_type,
                group_topic_type=group_topic_type,
                participant_topic_types=participant_topic_types,
                participant_descriptions=participant_descriptions,
                termination_condition=self._termination_condition,
            ),
        )
        # Add subscriptions for the group chat manager.
        await runtime.add_subscription(
            TypeSubscription(topic_type=group_chat_manager_topic_type, agent_type=group_chat_manager_agent_type.type)
        )
        await runtime.add_subscription(
            TypeSubscription(topic_type=group_topic_type, agent_type=group_chat_manager_agent_type.type)
        )
        await runtime.add_subscription(
            TypeSubscription(topic_type=team_topic_type, agent_type=group_chat_manager_agent_type.type)
        )

        output_messages: List[InnerMessage | ChatMessage] = []
        output_message_queue: asyncio.Queue[InnerMessage | ChatMessage | None] = asyncio.Queue()

        async def collect_output_messages(
            _runtime: AgentRuntime,
            id: AgentId,
            message: InnerMessage | ChatMessage,
            ctx: MessageContext,
        ) -> None:
            output_messages.append(message)
            await output_message_queue.put(message)

        await ClosureAgent.register(
            runtime,
            type="collect_output_messages",
            closure=collect_output_messages,
            subscriptions=lambda: [
                TypeSubscription(topic_type=output_topic_type, agent_type="collect_output_messages"),
            ],
        )

        # Start the runtime.
        runtime.start()

        # Run the team by publishing the task to the team topic and then requesting the result.
        team_topic_id = TopicId(type=team_topic_type, source=self._team_id)
        group_chat_manager_topic_id = TopicId(type=group_chat_manager_topic_type, source=self._team_id)
        first_chat_message = TextMessage(content=task, source="user")
        output_messages.append(first_chat_message)
        await output_message_queue.put(first_chat_message)
        await runtime.publish_message(
            GroupChatPublishEvent(agent_message=first_chat_message),
            topic_id=team_topic_id,
        )
        await runtime.publish_message(GroupChatRequestPublishEvent(), topic_id=group_chat_manager_topic_id)

        # Start a coroutine to stop the runtime and signal the output message queue is complete.
        async def stop_runtime() -> None:
            await runtime.stop_when_idle()
            await output_message_queue.put(None)

        shutdown_task = asyncio.create_task(stop_runtime())

        # Yield the messsages until the queue is empty.
        while True:
            message = await output_message_queue.get()
            if message is None:
                break
            yield message

        # Wait for the shutdown task to finish.
        await shutdown_task

        # Yield the final result.
        yield TaskResult(messages=output_messages)
