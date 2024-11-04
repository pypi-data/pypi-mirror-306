from typing import List

from src.agents.tools import AnthropicTool

__all__ = []


def create_read_previous_messages_tool(conversation: list[str]):

    def read_previous_messages_in_conversation(num_messages: int):
        return conversation[-num_messages:]

    return AnthropicTool(
        name="Read_Previous_Conversation_Messages",
        function=read_previous_messages_in_conversation,
        description="""Fetch the last n messages in the conversation""")


def create_read_all_conversation_messages_tool(conversation: list[str]):

    def read_all_messages_in_conversation():
        return '\n\n'.join(conversation)

    return AnthropicTool(
        name="Read_All_Conversation_Messages",
        function=read_all_messages_in_conversation,
        description="""Fetch all messages in the conversation""")


if __name__ == "__main__":
    tool = create_read_previous_messages_tool(['a', 'b'])
    print(tool)

    print(tool.input_schema)
    print(tool.function(2))
