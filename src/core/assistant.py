from src.ai_engine.provider import DemoAIProvider
from src.memory.store import MemoryStore


class ConoriAssistant:
    """Coordena a conversa, o motor de IA e a memória local."""

    def __init__(self) -> None:
        self.memory = MemoryStore()
        self.provider = DemoAIProvider()

    def respond(self, message: str) -> str:
        cleaned = message.strip()
        if not cleaned:
            return "Pode escrever ou dizer algo para começarmos."
        self.memory.save("user", cleaned)
        answer = self.provider.generate(cleaned)
        self.memory.save("assistant", answer)
        return answer

    def recent_history(self, limit: int = 10):
        return self.memory.recent(limit=limit)
