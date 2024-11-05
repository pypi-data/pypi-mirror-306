from enum import Enum
from typing import List

from InquirerPy import prompt
from rich.console import Console

CONSOLE = Console()


class PROMPT_SELECTION_TYPE(Enum):
    TEAM = "team"
    SERVICE = "service"
    CATALOG = "catalog"
    IMAGE = "image"


def prompt_for_selection(items: List[str], selection_type: PROMPT_SELECTION_TYPE) -> int:
    type_str = selection_type.value
    questions = [
        {
            "type": "list",
            "name": type_str,
            "message": f"Which {type_str} do you want to switch to?",
            "choices": [{"name": t, "value": i} for i, t in enumerate(items)],
        }
    ]
    answers = prompt(questions)
    return answers[type_str]
