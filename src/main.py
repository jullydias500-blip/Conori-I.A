from src.core.assistant import ConoriAssistant
from src.interface.cli import run_cli


def main() -> None:
    assistant = ConoriAssistant()
    run_cli(assistant)


if __name__ == "__main__":
    main()
