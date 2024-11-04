import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from src.agents.messages import (
    AbstractLLMMessage,
    LLMMessage,
    ToolInvoked,
    ToolNotInvoked,
)
from src.config.project_paths import application_data_dir
from src.conversations.messages import ConversationMessage
from src.telemetry.common import load_json_from_disk, save_jsonlist_to_disk

log = logging.getLogger(__name__)


class LLMConversationTelemetry:

    def get_filepath(self, conversation_name: str):
        return application_data_dir / 'conversations' / f"{conversation_name}_messages.json"

    def store_conversation_history(
        self,
        conversation_name: str,
        messages: Sequence[ConversationMessage],
    ):
        data = [i.to_dict() for i in messages]

        save_jsonlist_to_disk(data, self.get_filepath(conversation_name))

    def store_introspection_message(
        self,
        conversation_name: str,
        message: ConversationMessage,
    ):
        history = self.get_conversation_history(conversation_name)
        history.append(message.to_dict())
        save_jsonlist_to_disk(history, self.get_filepath(conversation_name))

    def get_conversation_history(
        self,
        conversation_name: str,
    ):
        """
        Retrieve all messages for the specified agent.
        """

        messages = load_json_from_disk(
            filepath=self.get_filepath(conversation_name))
        return messages

    def get_all(self):
        dirpath = self.get_filepath('').parent
        files = os.listdir(dirpath)
        conversations = [
            f.split("_")[0] for f in files if f.endswith("_messages.json")
        ]
        return conversations
