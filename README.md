# Conori I.A. 🌿

Assistente de inteligência artificial inspirada na floresta amazônica.

A Conori é um projeto modular, multiplataforma e de funcionamento híbrido (online/offline). Esta base representa o início da **versão 0.1**: estrutura organizada, interface de terminal, memória local simples e uma camada inicial para conectar motores de IA.

> **Estado real do projeto:** esta versão é um protótipo inicial. Reconhecimento de voz, palavra de ativação, síntese de voz, integração com provedores de IA e autonomia avançada ainda precisam ser implementados e testados.

## Visão do projeto

- Identidade visual e personalidade próprias.
- Arquitetura modular para facilitar a evolução.
- Funcionamento híbrido: recursos locais e serviços online.
- Memória persistente local, com controle do usuário.
- Voz com ativação por botão e palavra de ativação (planejada).
- Aplicação multiplataforma, com futura interface desktop e mobile.

## Requisitos

- Python 3.10 ou superior.
- Não é necessária chave de API para executar o modo de demonstração.

## Executar

Na pasta do projeto:

```bash
python -m venv .venv
```

Ativar o ambiente:

**Windows**
```powershell
.venv\Scripts\activate
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Iniciar:

```bash
python -m src.main
```

A memória local é criada em `data/conori_memory.sqlite3` na primeira execução.

## Estrutura

```text
src/
  main.py              # ponto de entrada
  core/                # coordenação da aplicação
  ai_engine/           # adaptadores de inteligência artificial
  memory/              # memória persistente local
  voice/               # interfaces futuras de voz
  interface/           # interface inicial de terminal
  config/              # configurações
assets/
  images/              # identidade visual
  audio/               # voz oficial, quando adicionada
  icons/
docs/                  # planejamento e arquitetura
tests/                 # testes automatizados
data/                  # dados locais (não versionados)
```

## Segurança e privacidade

- Nunca coloque chaves de API, senhas ou tokens no GitHub.
- Arquivos `.env`, banco de dados local e dados pessoais são ignorados pelo Git.
- Ações externas, compras, envios, exclusões e operações sensíveis devem exigir confirmação explícita.
- A memória local deve ser transparente e permitir inspeção e exclusão pelo usuário.

## Roadmap

Consulte:
- [`docs/planejamento-v01.md`](docs/planejamento-v01.md)
- [`docs/planejamento-v02.md`](docs/planejamento-v02.md)
- [`docs/arquitetura.md`](docs/arquitetura.md)
- [`docs/como-publicar-no-github.md`](docs/como-publicar-no-github.md)

## Licença

Ainda não definida. O repositório deve permanecer privado até a decisão sobre licença, direitos dos assets e política de distribuição.
