import logging
from dataclasses import dataclass
from typing import Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

# from src.teams.team import LLMTeam

log = logging.getLogger(__name__)


class LLMTeamProjectLink(SQLModel, table=True):
    src_id: int | None = Field(default=None,
                               foreign_key="team.id",
                               primary_key=True)
    project_id: int | None = Field(default=None,
                                   foreign_key="team.id",
                                   primary_key=True)


class LLMTeam(SQLModel):
    id: str | None = Field(default=None, primary_key=True)
    agents: list[str]
    manager: str

    description: str
    projects: list["Project"] = Relationship(back_populates="teams",
                                             link_model=LLMTeamProjectLink)


class Project(SQLModel):
    id: str | None = Field(default=None, primary_key=True)

    teams: list["LLMTeam"] = Relationship(back_populates="projects",
                                          link_model=LLMTeamProjectLink)

    task: str
    description: str
    acceptance_criteria: Optional[str]
