from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Contrato para conectar provedores online ou modelos locais."""

    @abstractmethod
    def generate(self, message: str) -> str:
        raise NotImplementedError


class DemoAIProvider(AIProvider):
    """Resposta demonstrativa; não é um modelo de IA real."""

    def generate(self, message: str) -> str:
        return (
            "Ainda estou na minha versão inicial de demonstração. "
            "Recebi sua mensagem: "
            f"“{message}”. "
            "Meu motor de IA real será conectado em uma próxima etapa."
        )


# Próximas implementações previstas:
# - OnlineAIProvider: integração com API, usando chave em variável de ambiente.
# - LocalAIProvider: integração com modelo executado no próprio dispositivo.
# - HybridAIProvider: seleção de provedor conforme conexão, privacidade e capacidade.
