import logging
from dataclasses import dataclass
from typing import List

from sqlmodel import SQLModel

from src.agents.basic_agent import LLMAgent

log = logging.getLogger(__name__)


@dataclass
class LLMTeam(SQLModel):
    agents: List[LLMAgent]
    manager: LLMAgent

    description: str
