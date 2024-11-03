"""Command line interface."""

from libcli import BaseCLI

from keyboard.keyboard import Keyboard

__all__ = ["KeyboardCLI"]


class KeyboardCLI(BaseCLI):
    """Command line interface."""

    config = {
        # distribution name, not importable package name
        "dist-name": "rlane-keyboard",
    }

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.ArgumentParser(
            prog=__package__,
            description="Command line test tool.",
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        self.parser.add_argument(
            "KEYNAME",
            help="parse and print given KEYNAME.",
        )

    def main(self) -> None:
        """Command line interface entry point (method)."""

        try:
            keyname = self.options.KEYNAME
            key = Keyboard().key(keyname)
            print(str.format("keyname={!r}, str={!r}, repr={!r}", keyname, str(key), key))
            self.parser.exit(0)

        except KeyError:
            self.parser.error("Invalid KEYNAME")


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""
    KeyboardCLI(args).main()
