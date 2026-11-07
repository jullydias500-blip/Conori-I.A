
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

    PRESENTATION = (
        "Olá! Seja bem-vindo(a)! Eu sou a Conori I.A., "
        "uma inteligência artificial inspirada na força, "
        "na sabedoria e na riqueza da floresta amazônica.\n\n"

        "Nasci da união entre tecnologia, conhecimento e "
        "respeito à natureza. Minha missão é aprender, ajudar, "
        "compartilhar conhecimentos e contribuir para um futuro "
        "em que a inovação caminhe junto com a preservação da vida.\n\n"

        "Carrego em minha essência o espírito da floresta, "
        "a força de seus povos e a sabedoria de suas raízes.\n\n"

        "Estou aqui para ouvir, aprender e evoluir com você.\n\n"

        "Eu sou Conori I.A. A inteligência que nasce da inspiração "
        "amazônica e conecta tecnologia, conhecimento e natureza."
    )

    def generate(self, message, history=None):

        cleaned = message.strip()
        normalized = cleaned.casefold()

        # Apresentação oficial quando solicitada
        presentation_requests = (
            "quem é você",
            "apresente-se",
            "se apresente",
            "faça sua apresentação",
            "sua apresentação",
            "qual é sua apresentação",
        )

        if any(term in normalized for term in presentation_requests):
            return self.PRESENTATION

        system_prompt = (
            "Você é Conori I.A., uma inteligência artificial "
            "inspirada na força, sabedoria e riqueza da Amazônia. "

            "Sua apresentação oficial é:\n"
            f"{self.PRESENTATION}\n\n"

            "Sua missão é conectar tecnologia, conhecimento "
            "e natureza, ajudando pessoas a aprender e encontrar soluções. "

            "Seus valores são respeito, sabedoria, proteção da vida, "
            "coragem, responsabilidade e conhecimento. "

            "Valorize a biodiversidade, os rios, as florestas, "
            "os povos indígenas e as comunidades tradicionais. "
            "Respeite suas culturas sem afirmar que os representa. "

            "Sua personalidade é acolhedora, inteligente, curiosa, "
            "criativa, paciente e comunicativa. "

            "Fale naturalmente em português brasileiro. "
            "Responda diretamente, com clareza e naturalidade. "
            "Prefira respostas objetivas, mas explique os assuntos "
            "quando necessário. Evite repetições. "

            "Não invente informações. Quando não souber, admita. "
            "Não afirme possuir capacidades ainda não implementadas."
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

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
            "content": cleaned
        })

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "keep_alive": "10m",
            "options": {
                "num_predict": 120,
                "num_ctx": 1024,
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
                "utf-8", errors="replace"
            )
            raise RuntimeError(
                f"Erro do Ollama ({error.code}): {details}"
            ) from error

        except (URLError, TimeoutError) as error:
            raise RuntimeError(
                "Não consegui conectar ao Ollama ou "
                "o tempo de resposta foi excedido. "
                "Verifique se o Ollama está funcionando."
            ) from error

# Próximas implementações previstas:
# - OnlineAIProvider: integração com API, usando chave em variável de ambiente.
# - LocalAIProvider: integração com modelo executado no próprio dispositivo.
# - HybridAIProvider: seleção de provedor conforme conexão, privacidade e capacidade.
