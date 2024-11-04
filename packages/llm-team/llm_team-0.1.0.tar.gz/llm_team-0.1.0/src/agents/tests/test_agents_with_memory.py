import unittest

from src.agents.agents_with_memory import ShortTermMemoryAgent


class TestShortTermMemoryAgent(unittest.TestCase):

    def setUp(self):
        self.agent = ShortTermMemoryAgent(name="TestAgent",
                                          prompt="Hello, I'm a test agent.")

    def test_serialization(self):
        serialized = self.agent.to_dict()
        del serialized['prompt']

        self.assertEqual(serialized, {"name": "TestAgent"})
        self.assertNotIn("_api_key", serialized)
        self.assertNotIn("_tracer", serialized)

    def test_deserialization(self):
        data = {
            "name": "DeserializedAgent",
            "prompt": "I'm a deserialized agent.",
            "extra_field": "This should be ignored"
        }
        deserialized_agent = ShortTermMemoryAgent.from_dict(data)
        self.assertEqual(deserialized_agent.name, "DeserializedAgent")
        self.assertFalse(hasattr(deserialized_agent, "extra_field"))

    def test_roundtrip(self):
        serialized = self.agent.to_dict()
        roundtrip_agent = ShortTermMemoryAgent.from_dict(serialized)
        self.assertEqual(self.agent.name, roundtrip_agent.name)

    def test_invalid_deserialization(self):
        with self.assertRaises(ValueError):
            ShortTermMemoryAgent.from_dict({"prompt": "Missing name field"})
