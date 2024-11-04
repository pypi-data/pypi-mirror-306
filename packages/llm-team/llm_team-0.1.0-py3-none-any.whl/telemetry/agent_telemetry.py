import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from src.agents.messages import (
    AbstractLLMMessage,
    LLMMessage,
    LLMToolUseDecision,
    ToolInvoked,
    ToolNotInvoked,
    ToolUsedOrFailed,
)
from src.config.project_paths import application_data_dir
from src.telemetry.common import load_json_from_disk, save_jsonlist_to_disk

log = logging.getLogger(__name__)


class LLMAgentTelemetry:

    def get_messages_filepath(self, agent_name: str):
        return application_data_dir / 'agents' / f"{agent_name}_messages.json"

    def get_tool_use_result_filepath(self, agent_name: str):
        return application_data_dir / 'agents' / f"{agent_name}_tool_use_results.json"

    def store_agent_messages(self,
                             messages: Sequence[AbstractLLMMessage],
                             conversation_id: Optional[str] = None):
        for i in messages:
            self.store_agent_message(i)

    def store_agent_message(
        self,
        message: AbstractLLMMessage,
    ):
        """
        Store a new message for the specified agent.
        """

        agent_name = message.creator.name

        log.info(f"saving message to chat {agent_name}")

        messages = load_json_from_disk(agent_name)
        messages.append(message.to_dict())

        save_jsonlist_to_disk(filepath=self.get_messages_filepath(agent_name),
                              messages=messages)

    def get_agent_messages(self, agent_name: str):
        """
        Retrieve all messages for the specified agent.
        """

        messages = load_json_from_disk(
            filepath=self.get_messages_filepath(agent_name))
        return messages

    def store_tool_use_results(
            self, agent_name: str,
            tool_use_results: list[tuple[LLMToolUseDecision,
                                         ToolUsedOrFailed]]):
        for i in tool_use_results:
            self.store_tool_use(agent_name=agent_name, tool_use=i)

    def store_tool_use(
        self,
        agent_name: str,
        tool_use: tuple[LLMToolUseDecision, ToolUsedOrFailed],
    ):

        messages = load_json_from_disk(
            self.get_tool_use_result_filepath(agent_name))

        decision, tool_use_result = tool_use
        context_behind_tool_use = decision.to_dict()
        tool_use_result_as_dict = tool_use_result.to_dict()

        messages.append(context_behind_tool_use)
        messages.append(tool_use_result_as_dict)

        save_jsonlist_to_disk(
            filepath=self.get_tool_use_result_filepath(agent_name),
            messages=messages)

    def get_previous_tool_uses(self, agent_name: str):
        return load_json_from_disk(
            filepath=self.get_tool_use_result_filepath(agent_name))

    def _get_all_agents_with_saved_msgs(self):
        data_dir = self.get_messages_filepath('').parent
        files = os.listdir(data_dir)

        agent_names = [
            f.split("_")[0] for f in files if f.endswith("_messages.json")
        ]
        return agent_names
