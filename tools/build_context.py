from pathlib import Path
import os

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".idea",
    ".vscode",
    ".aider",
    ".mypy_cache",
    "build",
    "dist",
}

IMPORTANT_FILES = [
    "README.md",
    "AGENTS.md",
    "pyproject.toml",
    "requirements.txt",
    "environment.yml",
    "environment.yaml",
    "setup.py",
]


def detect_language(root: Path) -> str:
    counts = {}

    extensions = {
        ".py": "Python",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C/C++",
        ".hpp": "C++",
        ".m": "MATLAB",
        ".ipynb": "Jupyter",
        ".cs": "C#",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".java": "Java",
    }

    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue

        if path.is_file():
            lang = extensions.get(path.suffix)
            if lang:
                counts[lang] = counts.get(lang, 0) + 1

    if not counts:
        return "Unknown"

    return max(counts, key=counts.get)


def directory_tree(root: Path, depth=2):
    lines = []

    def walk(path, prefix="", level=0):
        if level > depth:
            return

        items = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

        for item in items:
            if item.name in IGNORE_DIRS:
                continue

            lines.append(prefix + item.name)

            if item.is_dir():
                walk(item, prefix + "    ", level + 1)

    walk(root)
    return "\n".join(lines)


def main():

    project = Path(input("Project path: ").strip()).resolve()

    output = project / "PROJECT_CONTEXT.md"

    with output.open("w", encoding="utf8") as f:

        f.write(f"# Project Context\n\n")
        f.write(f"Project: {project.name}\n\n")

        f.write(f"Primary language: {detect_language(project)}\n\n")

        f.write("## Important files\n\n")

        for name in IMPORTANT_FILES:
            if (project / name).exists():
                f.write(f"- {name}\n")

        f.write("\n## Directory tree\n\n")
        f.write("```\n")
        f.write(directory_tree(project))
        f.write("\n```\n")

    print(f"\nCreated:\n{output}")


if __name__ == "__main__":
    main()