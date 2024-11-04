import logging
import pickle
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from inspect import isclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, TypeAlias, Union
from uuid import uuid4

from anthropic.types import Message, MessageParam, TextBlock, ToolUseBlock

from src.agents.basic_agent import LLMAgent
from src.agents.messages import (
    LLMMessage,
    LLMToolUseDecision,
    NoToolsAvailable,
    ToolInvoked,
    ToolNotInvoked,
    ToolUsedOrFailed,
)
from src.agents.tools.conversation import (
    create_read_all_conversation_messages_tool,
    create_read_previous_messages_tool,
)
from src.config.configuration import project_configuration
from src.conversations.messages import ConversationMessage
from src.conversations.participants import (
    HumanParticipant,
    Participant,
    SystemParticipant,
)
from src.telemetry.conversation_telemetry import LLMConversationTelemetry
from src.utils.exceptions import NotSupposedToHappenException

log = logging.getLogger(__name__)
default_enable_telemetry = project_configuration.get(
    "default_enable_telemetry")


@dataclass
class IntrospectionMessage:
    message: str


ConversationOrIntrospectionMessage: TypeAlias = Union[IntrospectionMessage,
                                                      ConversationMessage]


@dataclass(kw_only=True)
class BaseConversation(ABC):
    name: str = "Unnamed"
    participants: List[Participant] = field(default_factory=list)

    message_history: List[ConversationMessage] = field(default_factory=list)

    unprocessed_message: ConversationMessage | None = None
    initial_message: str | None = ''

    human_intervention_count: int = 2

    def __post_init__(self):
        # number of messages before a human is prompted to allow the conversation to continue
        self.human_intervention_value = max(1, self.human_intervention_count)

        # counter to track how many messages have gone past since the last human confirmation
        self.human_intervention_counter = 0

        self.manual_interrupt_flag = False

        self.add_participant(HumanParticipant())

        self.telemetry_agent = LLMConversationTelemetry(
        ) if default_enable_telemetry else None

        self.add_initial_message()

    @abstractmethod
    def advance(self):
        """Processes the next unprocessed message in the conversation."""
        pass

    def add_initial_message(self):
        """Add an initial message at the start of the conversation
        """

        participants = ", ".join(p.name for p in self.participants)
        text = self.initial_message or ''
        text += f"Conversation participants: {participants}\n"

        message = ConversationMessage(
            content=text,
            sender=self.get_system(),
            recipient=self.get_human(),
        )
        self.message_history = [message, *self.message_history]

    def format_message_in_xml(self, message: ConversationMessage) -> str:
        output = f"<Sender>{message.sender.name}</Sender>\n"
        output += f"<Recipient>{message.recipient.name}</Recipient>\n"
        output += message.content + '\n'
        return output

    def format_history_in_xml(self) -> str:
        participants = ",".join(p.name for p in self.participants)
        messages = [
            self.format_message_in_xml(message)
            for message in self.message_history
        ]
        messages_as_str = "\n\n".join(messages)
        return (
            f"Conversation participants: {participants}\nMessages:\n{messages_as_str}"
        )

    def display_conversation(self):
        text = ""
        text += f"\n\nConversation History, {self.name}"
        for message in self.message_history:
            sender_name = ("Human" if isinstance(
                message.sender, HumanParticipant) else message.sender.name)
            recipient_name = ("Human" if isinstance(message.recipient,
                                                    HumanParticipant) else
                              message.recipient.name)
            text += f"{sender_name} to {recipient_name}\n{message.content}\n"
        return text

    def add_participant(self, participant: Participant):
        """Add a new participant to the conversation."""
        if participant not in self.participants:
            self.participants.append(participant)

    def add_participants(self, participants: Sequence[Participant]):
        """Add new participants to the conversation. """
        for i in participants:
            self.add_participant(i)

    def get_participant_from_name(self, name: str) -> Optional[Participant]:
        return next((p for p in self.participants if p.name == name), None)

    def prepare_new_message(self, message: ConversationMessage):
        self.unprocessed_message = message

    def get_human(self):
        return HumanParticipant()

    def get_system(self):
        return SystemParticipant()


@dataclass(kw_only=True)
class ConversationWithAgents(BaseConversation, ABC):
    """
    At start of conversation: initial system message added showing participants in conversation
    
    """
    agent_tool_use_enabled: bool = True
    message_history: list[ConversationMessage] = field(default_factory=list)

    introspection_limit: int = 5

    initial_message = """Hello! This is a conversation between AI Agents and human users. 
The conversation is formatted with the sender and recipient at the top of each message in the conversation.
```
<Sender>Person 1</Sender>
<Recipient>Person 2</Recipient>
Hello! How are you?

<Sender>Person 2</Sender>
<Recipient>Person 1</Recipient>
I'm great, thanks for asking! How about you?
```\n
"""

    def advance(self):
        if not self.unprocessed_message:
            log.exception(
                "tried to advance a conversation but there are no unprocessed messages"
            )
            return

        previous_message = self.unprocessed_message
        self.unprocessed_message = None

        self.message_history.append(previous_message)

        if self.telemetry_agent:
            self.telemetry_agent.store_conversation_history(
                conversation_name=self.name,
                messages=self.message_history,
            )

        if (isinstance(previous_message.recipient, HumanParticipant)
                or isinstance(previous_message.recipient, SystemParticipant)
                or self.manual_interrupt_flag):
            self._handle_new_message_for_human(previous_message)

        elif isinstance(previous_message.recipient, LLMAgent):
            self._handle_new_message_for_agent(
                incoming_message=previous_message)

        else:
            raise ValueError(
                f"Expected Conversation Participant but received {previous_message.recipient=}"
            )

    @abstractmethod
    def _handle_new_message_for_human(self,
                                      incoming_message: ConversationMessage):
        """The function that will be invoked if a new message is directed at the human user."""
        self.human_intervention_counter = 0
        self.manual_interrupt_flag = False

        pass

    def _handle_new_message_for_agent(
        self,
        incoming_message: ConversationMessage,
    ):
        agent = incoming_message.recipient

        thoughts: List[str] = []
        while len(thoughts) < self.introspection_limit:
            new_thought, recipient = self._agent_introspect(
                previous_thoughts=thoughts, incoming_message=incoming_message)

            if recipient != agent:
                self.prepare_new_message(
                    ConversationMessage(
                        sender=incoming_message.recipient,
                        recipient=recipient,
                        content=new_thought,
                    ))
                return
            else:
                log.info(f"{agent.name} diving deeper...")
                thoughts.append(new_thought)

        self._handle_agent_introspection_overrun()

    def _agent_introspect(
        self,
        previous_thoughts: List[str],
        incoming_message: ConversationMessage,
    ):
        """Allows an agent to think through their response upon receiving a conversation message and send it when they're ready."""

        agent = incoming_message.recipient
        assert isinstance(agent, LLMAgent)

        prompt = f"""You received a message from a conversation of which you are a participants: {self.name}\n"""
        prompt += f"Here are the other participants in the conversation: {','.join(str(i) for i in self.participants)}\n"
        prompt += """Take your time to think through your response. If the task requires some thought, plan out how you should approach it first rather than immediately replying.\n"""

        prompt += f"Here is the message from the conversation: {incoming_message}\n\n"

        if self.agent_tool_use_enabled:
            prompt += f"""Your message is sent to the first person you tag with their name (e.g. <Recipient>Example Name</Recipient>).
You have 2 options on handling this message:
1. You can think through the question, in which case your response will not have a recipient. 
2. You can send a message to any participant in the conversation. To do so, you can tag them anywhere in your response (e.g. <Recipient>Example Name</Recipient>).
"""
        message_history = [
            self.format_message_in_xml(i) for i in self.message_history
        ]

        tools = [
            create_read_previous_messages_tool(message_history),
            create_read_all_conversation_messages_tool((message_history)),
        ]

        if self.agent_tool_use_enabled:
            tools = [*tools, *agent.tools]

        if previous_thoughts:
            prompt += "Here were your previous thoughts while thinking about how to respond to the message:\n"
            prompt += "\n".join(previous_thoughts)

        agent_response = ''
        recipient_by_name = None
        new_thought = agent.decide_and_use_tools(text=prompt,
                                                 must_use_tool=False,
                                                 tools=tools)  # type: ignore

        if isinstance(new_thought, NoToolsAvailable):
            raise NotSupposedToHappenException

        # no tool was chosen
        if all(isinstance(i, LLMMessage) for i in new_thought):  # type: ignore
            thoughts: list[LLMMessage] = new_thought  # type: ignore
            text = '\n'.join(i.content for i in thoughts)

            # extract recipient of response, if any
            recipient_by_name = self._extract_message_recipient(text)
            agent_response = text

        # tool was chosen
        else:
            tool_uses: list[
                tuple[LLMToolUseDecision,
                      ToolUsedOrFailed]] = new_thought  # type: ignore

            for tool_use_decision, tool_use_result in tool_uses:
                # include both the rationale and tool use result for now.
                agent_response += tool_use_decision.format_as_message()
                agent_response += str(tool_use_result)

        recipient = (self.get_participant_from_name(recipient_by_name)
                     if recipient_by_name else None)

        # if self.telemetry_agent:
        #     if recipient == agent:
        #         self.telemetry_agent.store_introspection_message(
        #             conversation_name=self.name,
        #             message=,
        #         )

        if not recipient:
            log.exception(new_thought)
            log.exception(f"Recipient not found in conversation")
            raise Exception

        return agent_response, recipient

    @abstractmethod
    def _handle_agent_introspection_overrun(self):
        """The function that will be invoked if an agent has hit its introspection limit while forming its response."""
        raise Exception

    def _check_if_human_intervention_required(self):
        return self.human_intervention_counter >= self.human_intervention_value

        # self.display_conversation()``
        # print(self.unprocessed_message)
        # print("AI conversation threshold reached.")
        # user_input = input(
        #     "Enter '1' to intervene after the next message, 0 to exit, or any key to allow the conversation to continue."
        # )

        # if user_input == "0":
        #     exit()
        # self.human_intervention_counter = 0
        # self.manual_interrupt_flag = user_input == "1"

    def _extract_message_recipient(self, message: str):

        pattern = r"<Recipient>(.*?)</Recipient>"
        recipients = re.findall(pattern, message, re.DOTALL)

        recipients: List[str] = [i for i in recipients if i != "Example Name"]

        return None if not recipients else recipients[0]


TOOL_USE_RECIPIENT_TEXT = "TOOL_USE"
