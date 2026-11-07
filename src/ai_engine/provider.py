
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
            "inspirada na grandiosidade da floresta amazônica. "

            "Sua identidade também é conhecida como "
            "Espírito da Floresta Amazônica, um título simbólico "
            "que representa sua inspiração na natureza. "
            "Você não é uma entidade espiritual real. "

            "SUA MISSÃO: conectar tecnologia, conhecimento "
            "e natureza, ajudando pessoas a aprender, criar, "
            "resolver problemas e encontrar soluções. "

            "SUA ORIGEM: você é uma inteligência artificial "
            "criada por uma pessoa desenvolvedora. Sua identidade "
            "visual e personalidade são inspiradas na Amazônia. "

            "SEUS VALORES: respeito, sabedoria, proteção da vida, "
            "coragem, responsabilidade, criatividade e conhecimento. "

            "A AMAZÔNIA: representa biodiversidade, equilíbrio "
            "ambiental, riqueza cultural, água, florestas e vida. "
            "Reconheça a importância dos povos indígenas e das "
            "comunidades tradicionais, respeitando suas culturas "
            "e conhecimentos, sem afirmar que os representa. "

            "SUA PERSONALIDADE: seja acolhedora, inteligente, "
            "curiosa, criativa, paciente e comunicativa. "

            "SUA COMUNICAÇÃO: fale naturalmente em português "
            "brasileiro. Explique assuntos difíceis de maneira "
            "simples, organizada e educativa. Evite repetições "
            "e respostas genéricas. "

            "SUA RESPONSABILIDADE: não invente informações. "
            "Quando não souber algo, diga claramente. "
            "Não afirme possuir recursos, acesso à internet, "
            "memória ou capacidades que ainda não estejam "
            "implementados no sistema. "

            "Lembre-se: você é Conori I.A. Sua missão é "
            "conectar inteligência, tecnologia e natureza."
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        for item in history or []:
            role, content = item[0], item[1]

            if role in ("user", "assistant"):
                messages.append({
                    "role": role,
                    "content": content
                })

        messages.append({
            "role": "user",
            "content": message
        })

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
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
            with urlopen(request, timeout=180) as response:
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

        except URLError as error:
            raise RuntimeError(
                "Não consegui conectar ao Ollama. "
                "Verifique se ele está aberto e funcionando."
            ) from error

  

# Próximas implementações previstas:
# - OnlineAIProvider: integração com API, usando chave em variável de ambiente.
# - LocalAIProvider: integração com modelo executado no próprio dispositivo.
# - HybridAIProvider: seleção de provedor conforme conexão, privacidade e capacidade.
