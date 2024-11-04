import logging

import pytest
from peewee import *

from src.agents.tools.base_tool import AnthropicTool, get_all_exported_tools
from src.database.db import db

log = logging.getLogger(__name__)


def mock_tool_function(param1: str, param2: int) -> str:
    return f"{param1} - {param2}"


class TestAnthropicTool:

    @pytest.fixture
    def sample_tool(self):
        return AnthropicTool("TestTool", "A test tool", mock_tool_function)

    def test_initialization(self, sample_tool):
        assert sample_tool.name == "TestTool"
        assert sample_tool.description == "A test tool"
        assert sample_tool.function == mock_tool_function

    def test_to_dict(self, sample_tool):
        tool_dict = sample_tool.to_dict()
        assert tool_dict["name"] == "TestTool"
        assert tool_dict["description"] == "A test tool"
        assert tool_dict["function"] == "mock_tool_function"
        assert "input_schema" in tool_dict

    def test_from_dict(self, sample_tool):
        tool_dict = sample_tool.to_dict()
        reconstructed_tool = AnthropicTool.from_dict(
            data=tool_dict, possible_tools={sample_tool.name: sample_tool})
        assert reconstructed_tool.name == sample_tool.name
        assert reconstructed_tool.description == sample_tool.description
        assert reconstructed_tool.input_schema == sample_tool.input_schema

    def test_format_for_anthropic_api(self, sample_tool):
        api_format = sample_tool.format_for_anthropic_api()
        assert "name" in api_format
        assert "description" in api_format
        assert "input_schema" in api_format

    def test_get_all_exported_tools(self):
        tools = get_all_exported_tools()
        assert isinstance(tools, dict)
        assert all(isinstance(tool, AnthropicTool) for tool in tools.values())

    def test_equality_and_hashing(self, sample_tool):
        identical_tool = AnthropicTool("TestTool", "A different description",
                                       mock_tool_function)
        assert sample_tool == identical_tool
        assert hash(sample_tool) == hash(identical_tool)

        different_tool = AnthropicTool("DifferentTool", "A test tool",
                                       mock_tool_function)
        assert sample_tool != different_tool
        assert hash(sample_tool) != hash(different_tool)


if __name__ == "__main__":

    logging.basicConfig(
        format="%(name)s-%(levelname)s|%(lineno)d:  %(message)s",
        level=logging.INFO)
    pytest.main([__file__, "-s"])
