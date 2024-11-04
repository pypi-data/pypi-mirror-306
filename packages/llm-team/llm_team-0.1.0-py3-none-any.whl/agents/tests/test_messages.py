from unittest.mock import Mock

import pytest
from anthropic.types import Message as AnthropicMessage
from anthropic.types import Usage

from src.agents.basic_agent import LLMAgent
from src.agents.messages import LLMMessage, LLMMessage_Generation_Metadata


@pytest.fixture
def sample_llm_agent():
    return Mock(spec=LLMAgent)


@pytest.fixture
def sample_generation_metadata():
    return LLMMessage_Generation_Metadata(
        message_id="test_id",
        model="claude-3-5-sonnet",
        input_tokens=100,
        output_tokens=50,
        stop_reason="stop_sequence",
        price_in_microcents=1000,
    )


@pytest.fixture
def sample_llm_message(sample_llm_agent, sample_generation_metadata):
    return LLMMessage(
        creator=sample_llm_agent,
        content="Test content",
        generation_batch_metadata=sample_generation_metadata,
    )


def test_llm_message_generation_metadata_to_dict(sample_generation_metadata):
    metadata_dict = sample_generation_metadata.to_dict()
    assert metadata_dict == {
        "_id": "test_id",
        "model": "claude-3-5-sonnet",
        "input_tokens": 100,
        "output_tokens": 50,
        "stop_reason": "stop_sequence",
        "price_in_microcents": 1000,
    }


def test_llm_message_to_dict(sample_llm_message, sample_llm_agent,
                             sample_generation_metadata):
    message_dict = sample_llm_message.to_dict()

    assert isinstance(message_dict["creator"], Mock)
    assert message_dict["creator"]._spec_class == LLMAgent
    assert message_dict["content"] == "Test content"
    assert message_dict[
        "generation_metadata"] == sample_generation_metadata.to_dict()


def test_llm_message_generation_metadata_from_anthropic_message():
    mock_anthropic_message = Mock(spec=AnthropicMessage)
    mock_anthropic_message.id = "anthropic_test_id"
    mock_anthropic_message.model = "claude-3-5-sonnet"
    mock_anthropic_message.stop_reason = "length"
    mock_anthropic_message.usage = Usage(input_tokens=200, output_tokens=100)

    metadata = LLMMessage_Generation_Metadata.from_anthropic_message(
        mock_anthropic_message)

    assert metadata.message_id == "anthropic_test_id"
    assert metadata.model == "claude-3-5-sonnet"
    assert metadata.stop_reason == "length"
    assert metadata.input_tokens == 200
    assert metadata.output_tokens == 100
    assert metadata.price_in_microcents is None


def test_calculate_price_of_generation():
    metadata = LLMMessage_Generation_Metadata(message_id="test_id",
                                              model="claude-3-5-sonnet",
                                              input_tokens=1000,
                                              output_tokens=500)

    price_in_microcents = LLMMessage_Generation_Metadata.calculate_price_of_generation(
        model=metadata.model,
        input_tokens=metadata.input_tokens,
        output_tokens=metadata.output_tokens)

    # Expected price:
    # Input: 1000 * 300 / 1,000,000 = 0.3 cents
    # Output: 500 * 1500 / 1,000,000 = 0.75 cents
    # Total: (0.3 + 0.75) * 1,000,000 microcents = 1,050,000 microcents

    assert price_in_microcents == 1050000


def test_calculate_price_of_generation_unknown_model():
    metadata = LLMMessage_Generation_Metadata(message_id="test_id",
                                              model="unknown-model",
                                              input_tokens=1000,
                                              output_tokens=500)

    price_in_microcents = LLMMessage_Generation_Metadata.calculate_price_of_generation(
        model=metadata.model,
        input_tokens=metadata.input_tokens,
        output_tokens=metadata.output_tokens)

    assert price_in_microcents is None
