import logging

from src.agents.basic_agent import LLMAgent

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

incoming_message = """How many planets are there in the solar system?"""

name = "Question and Answer"
participants = "Human"

prompt = f"""You received a message from a conversation of which you are a participants: {name}\n"""
prompt += f"Here are the other participants in the conversation: {','.join(str(i) for i in participants)}\n"
prompt += """Take your time to think through your response. If the task requires some thought, plan out how you should approach it first rather than immediately replying.\n"""

prompt += f"Here is the message from the conversation: {incoming_message}\n\n"

if True:
    prompt += f"""Your message is sent to the first person you tag with their name (e.g. <Recipient>Example Name</Recipient>).

You have 2 options on handling this message:
1. You can think through the question, in which case your response will not have a recipient.
2. You can send a message to any participant in the conversation. To do so, you can tag them anywhere in your response (e.g. <Recipient>Example Name</Recipient>).
"""

agent = LLMAgent(
    name="Robert",
    prompt="",
)

response = agent.think(prompt)

# import logging
# from dataclasses import dataclass

# logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s',
#                     level=logging.INFO)
# log = logging.getLogger(__name__)

# from src.utils.serialization import SerializableMixin

# @dataclass
# class A(SerializableMixin):
#     pass
