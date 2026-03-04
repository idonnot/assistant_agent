from pathlib import Path
import yaml
from config.settings import PROMPT_DIR


def load_system_prompt(path=None) -> str:
    """
    Load system.yaml and convert it into a formatted system prompt string.
    """

    if path is None:
        path = Path(PROMPT_DIR).joinpath("system", "system.yaml")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sections = []
    for key, value in config.items():
        sections.append(f"# {key.replace('_', ' ').title()}\n{value}")

    return "\n\n".join(sections)
