from pathlib import Path
import subprocess


class ContextBuilder:

    def __init__(self, project):

        self.project = Path(project)


    def build(self):

        folder = self.project / ".research-copilot"

        folder.mkdir(exist_ok=True)

        output = folder / "PROJECT_CONTEXT.md"

        with output.open(
            "w",
            encoding="utf8"
        ) as f:

            f.write(
                f"# Project Context\n\n"
            )

            f.write(
                f"Project: {self.project.name}\n\n"
            )

            f.write(
                "## Directory\n\n```\n"
            )

            for path in self.project.rglob("*"):

                if any(
                    ignored in path.parts
                    for ignored in [
                        ".git",
                        ".venv",
                        "__pycache__"
                    ]
                ):
                    continue

                if path.is_file():

                    relative = path.relative_to(
                        self.project
                    )

                    f.write(
                        str(relative) + "\n"
                    )

            f.write("\n```\n")

        return output