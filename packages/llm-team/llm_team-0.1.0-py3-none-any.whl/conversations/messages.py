from dataclasses import asdict, dataclass
from typing import List

from anthropic.types import MessageParam, TextBlock, ToolUseBlock
from pydantic import BaseModel

from src.conversations.participants import HumanMessage, Participant
from src.utils.serialization import SerializableMixin


class ConversationMessageModel(BaseModel):
    """
    Pydantic model representing the serializable fields of an ConversationMessage.

    This model serves as a schema for serialization and deserialization of ConversationMessage instances.
    It includes only the fields that should be persisted when serializing an ConversationMessage.
    """

    sender: Participant
    content: List[str]
    recipient: Participant

    class Config:
        extra = "ignore"  # This will ignore any extra fields during deserialization


@dataclass
class ConversationMessage(SerializableMixin):
    sender: Participant
    content: str
    recipient: Participant

    def is_from_human(self):
        return self.sender in ('human', 'Human')

    def __str__(self) -> str:
        return f"""ConversationMessage from {self.sender.name} to {self.recipient.name}\n{self.content}"""
