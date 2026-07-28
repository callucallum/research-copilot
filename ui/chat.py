from textual.app import App
from textual.widgets import Header, Footer, Input, Markdown
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory
from backend.ollama_client import OllamaClient
from backend.session import ResearchSession
from backend.history import ChatHistory


class ResearchCopilot(App):

    CSS = """

    Screen{

        layout:vertical;

    }

    """

    def __init__(self):
        super().__init__()
        self.chat_history = ""

    def compose(self):

        yield Header()

        yield Markdown("", id="chat")

        yield Input(
            placeholder="Ask a question..."
        )

        yield Footer()

    def on_mount(self):

        self.client = OllamaClient()

        self.session = ResearchSession()

        self.prompt = Path(
            "prompts/research.md"
        ).read_text(
            encoding="utf8"
        )

        root = Tk()
        root.withdraw()

        folder = askdirectory(title="Select Project")

        root.destroy()

        if folder:

            self.session.load_project(folder)

            self.messages = self.session.history.load()

            chat = self.query_one("#chat", Markdown)

            self.chat_history = (
                f"# Research Copilot\n\n"
                f"**Project:** {folder}\n\n"
                f"**Context loaded:** {bool(self.session.project_context)}"
            )

            chat.update(self.chat_history)

            self.title = f"Research Copilot - {Path(folder).name}"

        else:

            self.title = "Research Copilot"

    async def on_input_submitted(self,event):

        chat = self.query_one("#chat", Markdown)

        self.chat_history += (
            f"\n\n## You\n\n{event.value}\n"
        )

        chat.update(self.chat_history)

        self.messages.append(
            {

                "role":"user",

                "content":event.value

            })

        self.session.history.save(
            self.messages
        )

        system = self.prompt

        if self.session.loaded:

            system += "\n\n"

            system += "PROJECT CONTEXT\n"

            system += self.session.project_context

        reply = self.client.ask(

            system,

            self.messages[1:],

            event.value

        )

        self.messages.append(
            {
                "role":"assistant",

                "content":reply
            }
        )

        self.session.history.save(
            self.messages
        )

        self.chat_history += (
            f"\n\n## Research Copilot\n\n{reply}\n"
        )

        chat.update(self.chat_history)

        event.input.value=""