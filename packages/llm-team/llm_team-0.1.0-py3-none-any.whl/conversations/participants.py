from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, List, Optional, TypeAlias, Union

from src.agents.basic_agent import LLMAgent
from src.utils.serialization import SerializableMixin

Participant: TypeAlias = Union[LLMAgent, 'HumanParticipant',
                               'SystemParticipant']
HumanMessage: TypeAlias = str


@dataclass
class SystemParticipant(SerializableMixin):

    def __init__(self) -> None:
        self.name = 'System'


@dataclass
class HumanParticipant(SerializableMixin):

    def __init__(self, ):
        self.name = 'Human'
