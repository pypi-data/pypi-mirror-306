import importlib
import logging
from typing import Optional

from click import Command, Context, MultiCommand, UsageError, command


class CLI(MultiCommand):
    # Update as needed
    COMMANDS = [
        "server",
        "config",
        "tokens",
        "paths",
    ]

    def list_commands(self, ctx: Context) -> list[str]:
        return self.COMMANDS

    def get_command(self, ctx: Context, cmd_name: str) -> Optional[Command]:
        if cmd_name not in self.COMMANDS:
            raise UsageError(f"Unknown command: {cmd_name}. Available commands: {', '.join(self.COMMANDS)}")
        module = importlib.import_module(f"bbsky.{cmd_name}")
        if hasattr(module, "cli"):
            return module.cli
        elif hasattr(module, "main"):
            return module.main
        raise ImportError(f"Module {cmd_name} does not have a cli or main function")


@command(cls=CLI)
def main() -> None:
    """Command line interface for bbsky."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
    )


if __name__ == """__main__""":
    main()
