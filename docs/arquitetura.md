# Arquitetura técnica — Conori I.A.

## Visão geral

A arquitetura é modular e separa interface, coordenação, inteligência artificial, memória e voz.

```text
Pessoa usuária
    |
Interface (terminal agora; GUI/mobile futuramente)
    |
Core / Assistant
    |-------- AI Engine
    |            |---- Provedor online (futuro)
    |            |---- Modelo local/offline (futuro)
    |
    |-------- Memory (SQLite local)
    |
    |-------- Voice (STT/TTS e wake word — futuro)
```

## Módulos

- `core`: coordena o fluxo da aplicação.
- `ai_engine`: contrato comum para provedores online e locais.
- `memory`: persistência local em SQLite.
- `voice`: ponto de integração futura para microfone, STT, TTS e palavra de ativação.
- `interface`: entrada e saída com a pessoa usuária.
- `config`: configurações por variáveis de ambiente.

## Estratégia híbrida

A camada `AIProvider` permitirá conectar diferentes motores sem acoplar a interface a um fornecedor específico. O roteador híbrido deverá considerar disponibilidade de rede, privacidade, latência, custo e capacidade do dispositivo.

## Segurança

- Segredos somente em variáveis de ambiente ou cofre seguro.
- Dados locais ignorados pelo Git.
- Permissões explícitas para microfone e arquivos.
- Confirmação antes de ações externas ou destrutivas.
- Logs sem conteúdo sensível por padrão.
