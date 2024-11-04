import unittest

from src.agents.basic_agent import LLMAgent


class TestLLMAgent(unittest.TestCase):

    def setUp(self):
        self.agent = LLMAgent("TestAgent", "Hello, I'm a test agent.")

    def test_serialization(self):
        serialized = self.agent.to_dict()
        self.assertEqual(serialized, {
            "name": "TestAgent",
            "prompt": "Hello, I'm a test agent."
        })
        self.assertNotIn("_api_key", serialized)
        self.assertNotIn("_tracer", serialized)

    def test_deserialization(self):
        data = {
            "name": "DeserializedAgent",
            "prompt": "I'm a deserialized agent.",
            "extra_field": "This should be ignored"
        }
        deserialized_agent = LLMAgent.from_dict(data)
        self.assertEqual(deserialized_agent.name, "DeserializedAgent")
        self.assertEqual(deserialized_agent.prompt,
                         "I'm a deserialized agent.")

        self.assertFalse(hasattr(deserialized_agent, "extra_field"))

    def test_roundtrip(self):
        serialized = self.agent.to_dict()
        roundtrip_agent = LLMAgent.from_dict(serialized)
        self.assertEqual(self.agent.name, roundtrip_agent.name)
        self.assertEqual(self.agent.prompt, roundtrip_agent.prompt)

    def test_invalid_deserialization(self):
        with self.assertRaises(ValueError):
            LLMAgent.from_dict({"prompt": "Missing name field"})
