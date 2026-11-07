from src.core.assistant import ConoriAssistant


def run_cli(assistant: ConoriAssistant) -> None:
    print("\n🌿 CONORI I.A. — protótipo 0.1")
    print("Digite 'sair' para encerrar. Digite 'historico' para ver a memória recente.\n")

    while True:
        try:
            message = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nConori: Até a próxima! 🌳")
            break

        if message.lower() in {"sair", "exit", "quit"}:
            print("Conori: Até a próxima! 🌳")
            break

        if message.lower() == "historico":
            for role, content, created_at in assistant.recent_history():
                print(f"[{created_at}] {role}: {content}")
            continue

        print(f"Conori: {assistant.respond(message)}\n")
