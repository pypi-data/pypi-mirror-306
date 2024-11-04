import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, NewType, Optional, Type, TypeVar

from src.agents.basic_agent import LLMAgent
from src.agents.tools import AnthropicTool
from src.agents.tools.base_tool import get_all_exported_tools, get_tool_by_name
from src.agents.utils.team_creator_utils import (
    create_agent_from_team_outline,
    parse_agents,
    parse_json_from_text,
    parse_workflow,
    retry,
)

logging.basicConfig(format="%(name)s-%(levelname)s|%(lineno)d:  %(message)s",
                    level=logging.DEBUG)
log = logging.getLogger(__name__)


def use_agent_to_prepare_team_outline(task: str):
    prompt = """Your task will be to identify the roles required for a working group to accomplish tasks given by users.
Analyze the task's complexity and requirements.
Identify key roles needed to accomplish the task efficiently.
For each role, define:
a. Title
b. Primary responsibility and main objectives

Determine optimal number of agents (2-5) based on task scope.
Ensure roles are distinct yet complementary.
Identify potential interactions between roles.
Suggest a high-level workflow for task completion.

Provide concise output, focusing on essential information for each role and their collective approach to the task.
Format your output like this, filling in the necessary details:
<Agent>
<Title></Title>
<Responsibility and Objectives></Responsibility and Objectives>
</Agent>

<Agent>
<Title></Title>
<Responsibility and Objectives></Responsibility and Objectives>
</Agent>

<Workflow>
</Workflow>
"""

    agent = LLMAgent(name="Team Creator", prompt=prompt)

    return agent.think(task)


def use_agent_to_assign_tools(task: str, agent_configs: list[dict],
                              possible_tools: List[AnthropicTool]):
    tools_as_text = "\n".join(str(i) for i in possible_tools)
    prompt = f"""A working group of AI agents has been assigned a task: 
{task}

These are the roles and responsibilities of the agents in the working group:
{agent_configs}

Here are a list of possible tools available to them: 
{tools_as_text}


Based on the task and the agent's individual role, suggest some tools that they will require to complete this task. Try to assign only the tools that each agent will require, but don't be excessively miserly as well.
Format your output as json, filling in the necessary details:
"""

    prompt += r"""{
example_agent1: [ToolName1, ToolName2],
example_agent2: [],
}
Ensure that your response is valid json.
"""
    agent = LLMAgent(name="Tool Assigner",
                     prompt=prompt,
                     model="claude-3-haiku-20240307")
    return agent.think(task)


def create_team_from_outline(task, team_outline_response: str):
    """If an outline (prepare_team_outline) has already been generated, use this function to create the Agent objects."""
    all_tools = get_all_exported_tools()
    all_tools_as_list = list(all_tools.values())

    agent_outlines = parse_agents(team_outline_response)
    workflow = parse_workflow(team_outline_response)

    agents: dict[str, LLMAgent] = {}
    for outline in agent_outlines:
        agent = create_agent_from_team_outline(outline)
        agents[agent.name] = agent
    tool_assignment_response = use_agent_to_assign_tools(
        task=task,
        agent_configs=agent_outlines,
        possible_tools=all_tools_as_list)

    response_as_text = "\n".join(i.content for i in tool_assignment_response)
    tool_assignment = parse_json_from_text(response_as_text)

    for agent_name, tool_names in tool_assignment.items():
        tools: List[AnthropicTool] = []
        for tool_name in tool_names:
            tool = get_tool_by_name(tool_name, all_tools_as_list)
            if tool:
                tools.append(tool)
        agents[agent_name].register_tools(*tools)
    return agents, workflow


def create_team(task: str):
    all_tools = get_all_exported_tools()
    all_tools_as_list = list(all_tools.values())

    team_outline_response = use_agent_to_prepare_team_outline(task)
    response_as_text = "\n".join(i.content for i in team_outline_response)

    agent_outlines = parse_agents(response_as_text)
    workflow = parse_workflow(response_as_text)

    agents: dict[str, LLMAgent] = {}
    for outline in agent_outlines:
        agent = create_agent_from_team_outline(outline)
        agents[agent.name] = agent
    tool_assignment_response = use_agent_to_assign_tools(
        task=task,
        agent_configs=agent_outlines,
        possible_tools=all_tools_as_list)

    response_as_text = "\n".join(i.content for i in tool_assignment_response)

    tool_assignment = parse_json_from_text(response_as_text)

    for agent_name, tool_names in tool_assignment.items():
        tools: List[AnthropicTool] = []
        for tool_name in tool_names:
            tool = get_tool_by_name(tool_name, all_tools_as_list)
            if tool:
                tools.append(tool)
        agents[agent_name].register_tools(*tools)
    return agents, workflow


# if __name__ == "__main__":
#     create_team_with_retry = retry(create_team, max_attempts=3, delay=1)

#     task = """I want to create a team to create a dense information packet/document to explain all the context required for a software project for future AI agents and human developers.
#     They should save their drafts, final document and any other artifacts in the /docs directory of the root of the project they are working on."""

#     agents, workflow = create_team_with_retry(task)
#     print(agents, workflow)

#     dest = Path(
#         r"D:\projects\testbed\open-llm-swe\src\teams\swe_team\agents.json")
#     dest.write_text(json.dumps([agent.to_dict() for agent in agents.values()]))

#     dest = Path(
#         r"D:\projects\testbed\open-llm-swe\src\teams\swe_team\workflow.txt")
#     dest.write_text(workflow)
