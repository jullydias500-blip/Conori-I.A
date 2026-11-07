
from src.ai_engine.provider import OllamaAIProvider
from src.memory.store import MemoryStore


class ConoriAssistant:

    def __init__(self):
        # Inicializa a memória persistente
        self.memory = MemoryStore()

        # Inicializa a inteligência artificial local
        self.provider = OllamaAIProvider(
            model="qwen2.5:1.5b"
        )

        # Quantidade de mensagens antigas enviadas ao modelo
        self.history_limit = 4

    def respond(self, message):
        cleaned = message.strip()

        if not cleaned:
            return "Conori: Digite uma mensagem para conversarmos."

        # Recupera apenas as últimas mensagens
        history = self.memory.recent(
            limit=self.history_limit
        )

        # Registra a pergunta do usuário
        self.memory.save("user", cleaned)

        try:
            # Solicita uma resposta à inteligência artificial
            answer = self.provider.generate(
                cleaned,
                history=history
            )

            if not answer:
                return "Conori: Não consegui gerar uma resposta."

            # Salva a resposta na memória
            self.memory.save("assistant", answer)

            return answer

        except RuntimeError as error:
            return f"Conori: {error}"

        except Exception as error:
            return (
                "Conori: Ocorreu um erro inesperado "
                f"durante a resposta: {error}"
            )

    def recent_history(self, limit=10):
        """Retorna o histórico recente da Conori."""
        return self.memory.recent(limit=limit)
