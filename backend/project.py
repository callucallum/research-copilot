from pathlib import Path


class Project:

    def __init__(self, root):

        self.root = Path(root)

    def read(self, relative):

        return (self.root / relative).read_text(
            encoding="utf8",
            errors="ignore"
        )

    def list_files(self):

        return sorted(

            p.relative_to(self.root)

            for p in self.root.rglob("*")

            if p.is_file()

        )