from pathlib import Path
from backend.context_builder import ContextBuilder
from backend.history import ChatHistory


class ResearchSession:

    def __init__(self):
        self.project_path = None
        self.project_context = ""

    def load_project(self, folder):

        self.project_path = Path(folder)

        possible_locations = [
            self.project_path / ".research-copilot" / "PROJECT_CONTEXT.md",
            self.project_path / "PROJECT_CONTEXT.md",
        ]

        for context in possible_locations:
            if context.exists():
                self.project_context = context.read_text(
                    encoding="utf8",
                    errors="ignore"
                )
                break

        if not self.project_context:

            builder = ContextBuilder(
                self.project_path
            )

            context = builder.build()

            self.project_context = context.read_text(
                encoding="utf8",
                errors="ignore"
            )

        self.history = ChatHistory(
            self.project_path
        )


    @property
    def loaded(self):
        return self.project_path is not None