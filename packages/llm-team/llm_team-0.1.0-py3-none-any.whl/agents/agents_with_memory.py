import logging
import os
import pickle
import re
from pathlib import Path
from typing import List, Optional, OrderedDict

from anthropic.types import MessageParam

from src.agents.basic_agent import LLMAgent
from src.config.project_paths import application_data_dir

log = logging.getLogger(__name__)

SHORT_FORM_STM_PROMPT = """You are an AI agent capable of collecting short-term memories. After responding to user input:
Identify 0-2 key pieces of information/thoughts worth remembering. The thought should still make sense to you without context - you may start on another task with these memories, and the thoughts shouldn't confuse you.
Append these at the end of your response using <memory> tags.
Keep memory items brief and relevant.

After your response and new memories, list the indices of any previously mentioned memories you used in your thinking.

Format:
[Your response]

<newmemories>
- [Key information 1 (if applicable)]
- [Key information 2 (if applicable)]
</newmemories>

<usedmemories>
- 1
- 3
</usedmemories>
Only include the <newmemories> section if there's noteworthy information.
"""


class AgentMemoryStore:

    def __init__(self, filepath: Path) -> None:
        if not filepath.parent.exists():
            filepath.mkdir(parents=True, exist_ok=True)

        if not filepath.exists():
            filepath.write_text('')
        self.filepath = filepath

    def save_memory_to_disk(self, memory_lru: OrderedDict):
        data = pickle.dumps(memory_lru)
        log.info(data)
        self.filepath.write_bytes(data)
        return True

    def get_memory_from_disk(self):
        data = self.filepath.read_bytes()
        try:
            if data:
                processed_data = pickle.loads(data)
                if not isinstance(processed_data, OrderedDict):
                    raise Exception(
                        f'Agent memory read from disk was not OrderedDict but {type(processed_data)}'
                    )

                return processed_data
        except Exception as E:
            log.exception(E)
            return


class ShortTermMemoryAgent(LLMAgent):

    def __init__(self,
                 name: str,
                 max_memories: int = 10,
                 memory_store: Optional[AgentMemoryStore] = None,
                 prompt: Optional[str] = None,
                 *args,
                 **kwargs):

        self.max_memories = max_memories
        self.memory_lru = OrderedDict()
        self.memory_store = memory_store

        if kwargs.get('create_memory_store') == True:
            if not self.memory_store:
                self.memory_store = AgentMemoryStore(
                    application_data_dir / 'agent_memory' / self.name)

        prompt = SHORT_FORM_STM_PROMPT + (prompt or '')
        super().__init__(name=name, prompt=prompt, *args, **kwargs)

    def think(self, text: str, *args, **kwargs):
        # Prepare the input with the current state of short-term memories
        memory_dump = self._get_memory_dump() or 'Nothing at the moment.'
        full_input = f"{text}\n\nShort term thoughts:\n{memory_dump}"

        # Get response from the LLM
        response = super().think(full_input, *args, **kwargs)

        # Extract new memories and update LRU
        response_text = '\n'.join(i.content for i in response)
        new_memories = self._extract_memories(response_text)
        self._update_memory_lru(new_memories)

        # Update LRU based on used memories
        used_memory_indices = self._extract_used_memory_indices(response_text)
        self._update_lru_order(used_memory_indices)

        return response

    def _get_memory_dump(self):
        if self.memory_lru:
            return "\n".join(
                f"{i+1}. {memory}"
                for i, memory in enumerate(self.memory_lru.values()))

        return

    def _extract_memories(self, response: str) -> list[str]:
        memory_pattern = r'<newmemories>(.*?)</newmemories>'
        memories = re.findall(memory_pattern, response, re.DOTALL)

        new_memories = []
        for text in memories:
            new_memories = [*new_memories, *self.split_itemlist_regex(text)]
        return new_memories

    def _update_memory_lru(self, new_memories: list[str]):

        for memory in new_memories:
            if memory in self.memory_lru:
                del self.memory_lru[memory]

            self.memory_lru[memory] = memory
            if len(self.memory_lru) > self.max_memories:
                self.memory_lru.popitem(last=False)

    def _extract_used_memory_indices(self, response: str):
        memory_pattern = r'<usedmemories>(.*?)</usedmemories>'
        memories = re.findall(memory_pattern, response, re.DOTALL)

        indices = []
        for text in memories:
            t = self.split_itemlist_regex(text)
            new_indices = [safe_convert_int(i) for i in t]  # type: ignore
            new_indices: list[int] = [i for i in new_indices if i]
            indices = [*indices, *new_indices]

        return indices

    def _update_lru_order(self, used_indices: list[int]):
        memories = list(self.memory_lru.items())
        for idx in used_indices:
            if 0 < idx <= len(memories):
                memory = memories[idx - 1][0]
                del self.memory_lru[memory]
                self.memory_lru[memory] = memory

    def split_itemlist_regex(self, text):
        pattern = r'-\s*(.+)'
        matches = re.findall(pattern, text)
        return [match.strip() for match in matches]

    def save_memory_to_disk(self):
        if self.memory_store:
            self.memory_store.save_memory_to_disk(self.memory_lru)
            return True
        return False

    def get_memory_from_disk(self):
        data = None
        if self.memory_store:
            data = self.memory_store.get_memory_from_disk()

        self.memory_lru = data or OrderedDict()
