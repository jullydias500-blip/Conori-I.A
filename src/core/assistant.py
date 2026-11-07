
from src.ai_engine.provider import OllamaAIProvider
from src.memory.store import MemoryStore


class ConoriAssistant:

    def __init__(self):
        self.memory = MemoryStore()

        self.provider = OllamaAIProvider(
            model="qwen2.5:1.5b"
        )

        self.history_limit = 4

    def respond(self, message):

        cleaned = message.strip()

        if not cleaned:
            return "Digite uma mensagem para conversarmos."

        history = self.memory.recent(
            limit=self.history_limit
        )

        self.memory.save("user", cleaned)

        try:
            answer = self.provider.generate(
                cleaned,
                history=history
            )

            if not answer:
                return "Não consegui gerar uma resposta."

            self.memory.save("assistant", answer)

            return answer

        except RuntimeError as error:
            return f"Não consegui responder: {error}"

        except Exception as error:
            return (
                "Ocorreu um erro inesperado: "
                f"{error}"
            )

    def recent_history(self, limit=10):
        return self.memory.recent(limit=limit)

