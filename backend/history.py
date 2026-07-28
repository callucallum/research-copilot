import json
from pathlib import Path


class ChatHistory:

    def __init__(self, project_path):

        self.file = (
            Path(project_path)
            / ".research-copilot"
            / "history.json"
        )

        self.file.parent.mkdir(
            exist_ok=True
        )


    def load(self):

        if not self.file.exists():
            return []

        return json.loads(
            self.file.read_text(
                encoding="utf8"
            )
        )


    def save(self, messages):

        self.file.write_text(
            json.dumps(
                messages,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf8"
        )