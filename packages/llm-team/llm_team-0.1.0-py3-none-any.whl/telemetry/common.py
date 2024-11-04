import json
import os
from pathlib import Path


def save_jsonlist_to_disk(messages: list[dict], filepath: Path):
    """takes a list of dicts and saves to disk"""
    filepath.parent.mkdir(exist_ok=True, parents=True)

    with open(filepath, "w") as f:
        json.dump(messages, f)


def load_json_from_disk(filepath):
    filepath.parent.mkdir(exist_ok=True, parents=True)

    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return []
