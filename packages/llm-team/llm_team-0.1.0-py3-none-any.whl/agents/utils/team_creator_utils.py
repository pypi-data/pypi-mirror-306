import inspect
import json
import logging
import re
import time
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar

from src.agents.basic_agent import LLMAgent

log = logging.getLogger(__name__)


def parse_agents(xml_string: str):
    """
    Parse the given XML-like string into a list of dictionaries.

    Each dictionary contains 'title' and 'responsibility_and_objectives' keys.

    Args:
    xml_string (str): The XML-like string containing agent information.

    Returns:
    List[Dict[str, str]]: A list of dictionaries, each representing an agent.

    Raises:
    AgentParserError: If the input is empty or not a string.
    """
    if not isinstance(xml_string, str):
        raise Exception("Input must be a string")
    if not xml_string.strip():
        raise Exception("Input string is empty")

    # Split the string into individual agent blocks
    agent_blocks = re.findall(r'<Agent>.*?</Agent>', xml_string, re.DOTALL)

    if not agent_blocks:
        return []  # Return an empty list if no agents are found

    agents: List[Dict[str, str]] = []
    for block in agent_blocks:
        agent = {}
        # Extract title
        title_match = re.search(r'<Title>(.*?)</Title>', block, re.DOTALL)
        agent['title'] = title_match.group(1).strip() if title_match else ""

        # Extract responsibility and objectives
        resp_match = re.search(
            r'<Responsibility and Objectives>(.*?)</Responsibility and Objectives>',
            block, re.DOTALL)
        agent['responsibility_and_objectives'] = resp_match.group(
            1).strip() if resp_match else ""

        agents.append(agent)

    return agents


def create_agent_from_team_outline(d: dict,
                                   agent_type: Type[LLMAgent] = LLMAgent,
                                   **kwargs):
    name = d['title']
    prompt = d['responsibility_and_objectives']

    try:
        return agent_type(name=name, prompt=prompt, **kwargs)
    except Exception as e:
        raise Exception(e)


def parse_workflow(xml_string: str):
    workflow_matches = list(
        re.finditer(r'<Workflow>(.*?)</Workflow>', xml_string, re.DOTALL))

    if not workflow_matches:
        raise Exception("No Workflow tag found in the XML string")

    # Take the first match
    first_match = workflow_matches[0]

    # Extract the content inside the Workflow tags
    workflow_block = first_match.group(1).strip()

    return workflow_block


def parse_json_from_text(text: str):
    """
    Extract and parse JSON from the given text.

    Args:
    text (str): The input text containing JSON.

    Returns:
    dict: Parsed JSON data.

    Raises:
    InvalidJSONError: If JSON is invalid or not found.
    """
    # Find JSON-like content (text between curly braces)
    json_match = re.search(r'\{.*\}', text, re.DOTALL)

    if not json_match:
        raise Exception("No JSON content found in the text.")

    json_str = json_match.group(0)

    try:
        # Parse the JSON string
        parsed_json: dict = json.loads(json_str)
        return parsed_json
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON: {str(e)}")


T = TypeVar('T')


def retry(func: Callable[..., T],
          max_attempts: int = 3,
          delay: float = 1) -> Callable[..., T]:
    """
    A wrapper function that retries the given function up to a specified number of times.

    Args:
    func (Callable): The function to be retried.
    max_attempts (int): The maximum number of attempts to make. Default is 3.
    delay (float): The delay in seconds between attempts. Default is 1 second.

    Returns:
    Callable: A wrapped version of the input function with retry capability.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        attempts = 0
        while attempts < max_attempts:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                if attempts == max_attempts:
                    raise  # Re-raise the last exception if all attempts fail
                log.info(
                    f"{func.__name__} attempt {attempts} failed. Reason: {e.args}. Retrying in {delay} seconds..."
                )
                time.sleep(delay)
        # This line should never be reached, but it's here to satisfy type checking
        raise RuntimeError("Unexpected error in retry logic")

    return wrapper
