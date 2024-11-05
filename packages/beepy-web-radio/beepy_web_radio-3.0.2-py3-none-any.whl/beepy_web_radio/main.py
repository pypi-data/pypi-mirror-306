from .cli import main as cli_main
from .tui import BeepyWebRadioApp


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        cli_main()
    else:
        BeepyWebRadioApp().run()


if __name__ == "__main__":
    main()
