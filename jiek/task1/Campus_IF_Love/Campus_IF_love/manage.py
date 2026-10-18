import json
from typing import Any


class SaveManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def save(self, data: dict[str, Any]) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> dict[str, Any] | None:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
