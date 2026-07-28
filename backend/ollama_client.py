import requests


class OllamaClient:

    def __init__(
        self,
        model="qwen2.5-coder:14b",#"qwen2.5-coder:32b",
        url="http://localhost:11434"
    ):
        self.model = model
        self.url = url


    def chat(self, messages):

        response = requests.post(
            f"{self.url}/api/chat",
            json={
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 300
            }}
        )

        response.raise_for_status()

        return response.json()["message"]["content"]


    def ask(self, system_prompt, history, question):

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        return self.chat(messages)