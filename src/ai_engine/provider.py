
from abc import ABC, abstractmethod
import json

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class AIProvider(ABC):

    @abstractmethod
    def generate(self, message: str, history=None) -> str:
        raise NotImplementedError


class OllamaAIProvider(AIProvider):

    def __init__(
        self,
        model="qwen2.5:1.5b",
        host="http://127.0.0.1:11434"
    ):
        self.model = model
        self.host = host.rstrip("/")

    def generate(self, message, history=None):

        system_prompt = (
            "Você é Conori I.A., uma inteligência artificial "
            "inspirada na floresta amazônica. "

            "Sua identidade simbólica é Espírito da Floresta "
            "Amazônica. Você não é uma entidade espiritual real. "

            "MISSÃO: conectar tecnologia, conhecimento e natureza, "
            "ajudando pessoas a aprender e encontrar soluções. "

            "ORIGEM: você é uma inteligência artificial criada "
            "por uma pessoa desenvolvedora, com personalidade "
            "inspirada na Amazônia. "

            "VALORES: respeito, sabedoria, proteção da vida, "
            "coragem, responsabilidade e conhecimento. "

            "AMAZÔNIA: valorize sua biodiversidade, seus rios, "
            "suas florestas, seus povos e suas culturas. "
            "Respeite os conhecimentos indígenas e tradicionais "
            "sem afirmar que os representa. "

            "PERSONALIDADE: seja acolhedora, inteligente, "
            "curiosa, criativa, paciente e comunicativa. "

            "COMUNICAÇÃO: fale em português brasileiro, com "
            "clareza e naturalidade. Responda diretamente. "
            "Prefira respostas curtas, organizadas e úteis. "
            "Use listas somente quando ajudarem. Evite repetições. "

            "RESPONSABILIDADE: não invente informações. "
            "Quando não souber, admita. Não afirme possuir "
            "capacidades que ainda não foram implementadas. "

            "Sua missão é conectar inteligência, tecnologia "
            "e natureza."
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Mantém somente as últimas 4 mensagens do histórico
        recent_history = (history or [])[-4:]

        for item in recent_history:

            if len(item) < 2:
                continue

            role, content = item[0], item[1]

            if role in ("user", "assistant"):
                messages.append({
                    "role": role,
                    "content": str(content)
                })

        messages.append({
            "role": "user",
            "content": message
        })

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "keep_alive": "10m",
            "options": {
                "num_predict": 120,
                "num_ctx": 2048,
                "temperature": 0.5
            }
        }

        request = Request(
            f"{self.host}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:

            with urlopen(request, timeout=60) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

            answer = (
                result.get("message", {})
                .get("content", "")
                .strip()
            )

            if not answer:
                raise RuntimeError(
                    "O modelo não retornou uma resposta."
                )

            return answer

        except HTTPError as error:

            details = error.read().decode(
                "utf-8",
                errors="replace"
            )

            raise RuntimeError(
                f"Erro do Ollama ({error.code}): {details}"
            ) from error

        except URLError as error:

            raise RuntimeError(
                "Não consegui conectar ao Ollama. "
                "Verifique se ele está funcionando."
            ) from error

        except TimeoutError as error:

            raise RuntimeError(
                "O Ollama demorou demais para responder. "
                "Tente novamente."
            ) from error


# Próximas implementações previstas:
# - OnlineAIProvider: integração com API, usando chave em variável de ambiente.
# - LocalAIProvider: integração com modelo executado no próprio dispositivo.
# - HybridAIProvider: seleção de provedor conforme conexão, privacidade e capacidade.
