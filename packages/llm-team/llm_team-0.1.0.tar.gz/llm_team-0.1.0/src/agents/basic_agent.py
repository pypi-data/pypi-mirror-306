import json
import logging
from abc import abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Type
from uuid import uuid4

from anthropic import Anthropic
from anthropic.types import MessageParam
from anthropic.types.text_block import TextBlock
from anthropic.types.tool_use_block import ToolUseBlock
from pydantic import BaseModel

from src.agents.messages import (
    LLMMessage,
    LLMToolUseDecision,
    NoToolsAvailable,
    ToolInvoked,
    ToolNotInvoked,
    ToolUsedOrFailed,
)
from src.agents.tools import AnthropicTool
from src.config.configuration import project_configuration
from src.config.project_secrets import ANTHROPIC_API_KEY
from src.telemetry.agent_telemetry import LLMAgentTelemetry

log = logging.getLogger(__name__)

ENABLE_AGENT_TELEMETRY = project_configuration.get("ENABLE_AGENT_TELEMETRY")


@dataclass(kw_only=True)
class LLMAgent():
    name: str
    prompt: str = ""
    model: str = "claude-3-5-sonnet-20240620"  # self.model = "claude-3-opus-20240229"

    api_key: str = ANTHROPIC_API_KEY
    tools: dict['AnthropicTool', Callable] = field(default_factory=dict)

    telemetry_handler = LLMAgentTelemetry() if ENABLE_AGENT_TELEMETRY else None

    def __post_init__(self):
        self.client = Anthropic(api_key=self.api_key)

        log.info(f"started agent {self.name}")

    def pre_think(
        self,
        text: str,
        response_prefix: Optional[str] = None,
        previous_messages: Optional[str] = None,
        **kwargs,
    ):
        """Invoked before a think.
        Use to manipulate the state of the Agent or the input to a think() method.
        Can be extended for child classes."""
        return text, response_prefix, previous_messages, kwargs

    def post_think(self, messages: Sequence[LLMMessage]):
        """Invoked after a think().\n
        Use to manipulate the output of the Agent.\n
        Can be extended for child classes. 
        """
        return messages

    def think(
        self,
        text: str,
        response_prefix: Optional[str] = None,
        previous_messages: Optional[str] = None,
        **kwargs,
    ):
        """
        Process the given prompt and return a response. Only text generation will be performed - guaranteed not to perform tool use.
            text: Main text content to send to LLM.
            response_prefix: Initial value in the LLM's output. Use to constrain the output.
            previous_messages: Text to send before the main body, but to be excluded from pre_think() and post_think() methods.
        """

        text, response_prefix, previous_messages, kwargs = self.pre_think(
            text=text,
            response_prefix=response_prefix,
            previous_messages=previous_messages,
            **kwargs,
        )

        max_tokens = kwargs.get("max_token") or 1024
        system_prompt = f"Your name is {self.name}.\n" + self.prompt

        messages = []
        previous_messages = previous_messages + "\n\n" if previous_messages else ""

        messages.append({
            "role": "user",
            "content": previous_messages + text,
        })

        # Add initial text to the response. Constrains the LLM's generated output
        if response_prefix:
            messages.append({
                "role": "assistant",
                "content": response_prefix,
            })
        log.debug(messages)

        response = self.client.messages.create(
            system=system_prompt,
            max_tokens=max_tokens,
            messages=messages,
            model=self.model,
        )
        messages = LLMMessage.from_anthropic_message(response, self)

        if response_prefix:
            metadata = messages[0].generation_batch_metadata
            first_message = LLMMessage(creator=self,
                                       content=response_prefix,
                                       generation_batch_metadata=metadata)
            messages.append(first_message)

        if self.telemetry_handler:
            self.telemetry_handler.store_agent_messages(messages)

        return self.post_think(messages)

    def decide_and_use_tools(
        self,
        text: str,
        must_use_tool: bool = True,
        tools: Optional[List[AnthropicTool]] = None,
        **kwargs,
    ):
        """
        Choose to use one or more tools from the list of tools provided. 
        
        Tools default to the agent's inventory if not set. 
        
        There are 3 possible return types of this function:
            1. If the agent has no tools available.
            2. If the agent chose not to invoke a tool (If the must_use_tool flag is set to false.)
            3. If the agent chose to use one or more tools - A list of the
        """

        max_tokens = kwargs.get("max_token") or 1024
        messages = [{"role": "user", "content": text}]

        system_prompt = self.prompt
        tools = tools or list(self.tools.keys())

        if not tools:
            return NoToolsAvailable

        # invoke api call to anthropic
        response = self.client.messages.create(
            system=system_prompt,
            max_tokens=max_tokens,
            messages=messages,  # type: ignore
            model=self.model,
            tool_choice={"type": "any"} if must_use_tool else {"type": "auto"},
            tools=[i.format_for_anthropic_api()
                   for i in tools],  # type: ignore
        )

        if not LLMToolUseDecision.decided_to_use_tool(response):
            return LLMMessage.from_anthropic_message(
                anthropic_message=response, creator=self)

        tool_use_decisions = LLMToolUseDecision.from_anthropic_message(
            anthropic_message=response, creator=self)

        if self.telemetry_handler:
            self.telemetry_handler.store_agent_messages(
                messages=tool_use_decisions)

        results: list[tuple[LLMToolUseDecision, ToolUsedOrFailed]] = []

        for decision in tool_use_decisions:
            result = self.use_tool(decision.tool_name, **decision.tool_kwargs)
            results.append((decision, result))

        if self.telemetry_handler:
            self.telemetry_handler.store_tool_use_results(
                agent_name=self.name,
                tool_use_results=results,
            )

        return results

    def interact(self, other_agent: "LLMAgent", message: str):
        """
        Interact with another agent by sending a message and receiving a response.
        """
        response = other_agent.think(f"{self.name} says: {message}")
        return response

    def register_tool(self, tool: AnthropicTool):
        """
        Register a new tool that the agent can use.
        """
        self.tools[tool] = tool.function

    def register_tools(self, *args: AnthropicTool):
        """
        Register a new tool that the agent can use.
        """
        for i in args:
            if isinstance(i, AnthropicTool):
                self.register_tool(i)
            else:
                raise ValueError

    def unregister_tool(self, tool: AnthropicTool):
        """
        Remove a tool from the agent's registry. Does not throw an error if the tool is not registered.
        """
        self.tools = {k: v for k, v in self.tools.items() if k != tool}

    def use_tool(self, tool_name: str,
                 tool_use_decision: Optional[LLMToolUseDecision], *args,
                 **kwargs):
        """
        Use a specified tool with given arguments.
        """

        tool = self.get_tool_from_name(tool_name)

        if not tool:
            return ToolNotInvoked(
                tool=None,
                tool_use_decision=tool_use_decision,
                reason=
                f"Tool {tool_name} not found in {self.name}'s collection of tools",
            )

        log.info(f"Using {self.tools[tool]}\nArgs:{args}\nKwargs:{kwargs}")
        try:
            result = self.tools[tool](*args, **kwargs)
            return ToolInvoked(tool=tool,
                               tool_use_decision=tool_use_decision,
                               result=result)
        except TypeError as e:
            log.exception(e)
            return ToolNotInvoked(tool=tool,
                                  tool_use_decision=tool_use_decision,
                                  reason=str(e))

    def get_tool_from_name(self, tool_name: str):
        tool = [i for i in self.tools if i.name == tool_name]
        if not tool:
            return
        return tool[0]

    def __str__(self) -> str:
        return f'LLMAgent {self.name}'

    def to_dict(self):
        return asdict(self)
