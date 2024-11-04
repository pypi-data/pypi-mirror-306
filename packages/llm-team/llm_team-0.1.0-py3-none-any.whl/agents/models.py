from peewee import *

from src.agents.tools.models import AnthropicToolModel
from src.database.db import BaseModel


class LLMAgentModel(BaseModel):
    name = CharField()
    prompt = CharField()
    model = CharField()


class AgentToToolLink:
    tool = ForeignKeyField(AnthropicToolModel)
    agent = ForeignKeyField(LLMAgentModel)


class LLMMessageModel:
    content = CharField()


class LLMToolUseDecisionModel:
    context = CharField()
    tool_name = CharField()
    tool_kwargs_json = CharField()


class ToolNotInvokedModel:
    tool_use_decision = ForeignKeyField(LLMToolUseDecisionModel)
    reason = CharField()


class ToolNotInvokedModelToToolLink:
    tool_not_invoked = ForeignKeyField(ToolNotInvokedModel)
    tool = ForeignKeyField(AnthropicToolModel)


class ToolInvokedModel:
    tool_use_decision = ForeignKeyField(LLMToolUseDecisionModel)
    result = CharField()


class LLMMessage_Generation_MetadataModel:
    message_id = CharField()
    model = CharField()
    input_tokens = DecimalField()
    output_tokens = DecimalField()
    stop_reason = CharField()
    price_in_microcents = DecimalField()
