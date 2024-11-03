import json
import os
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

import click
from attrs import define, evolve

from .data_cls import URL, structure, unstructure
from .paths import BBSKY_CONFIG_DIR, BBSKY_CONFIG_FILE


class SkyConfigError(Exception):
    pass


class SkyConfigEnvVars(Enum):
    CLIENT_ID = "BLACKBAUD_CLIENT_ID"
    CLIENT_SECRET = "BLACKBAUD_CLIENT_SECRET"
    REDIRECT_URI = "BLACKBAUD_REDIRECT_URI"
    SUBSCRIPTION_KEY = "BLACKBAUD_SUBSCRIPTION_KEY"

    @staticmethod
    def are_all_env_vars_set() -> bool:
        return all([os.getenv(var.value) for var in SkyConfigEnvVars])


def ensure_config_dir(func: Callable[..., Any]) -> Callable[..., Any]:
    """Ensure the config directory exists, and create it if it doesn't."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        BBSKY_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        return func(*args, **kwargs)

    return wrapper


@define(frozen=True, slots=True)
class SkyConfig:
    """
    Blackbaud app authentication credentials

    See this URL for helpful troubleshooting tips:
    https://developer.blackbaud.com/skyapi/docs/authorization/common-auth-issues

    client_id: str - Your Blackbaud client ID (should be same as app ID)
    client_secret: str - Your Blackbaud client secret (should be same as app secret)
    redirect_uri: URL - The URL you've pre-configured for the application
    subscription_key: str - Your Blackbaud subscription key
    """

    client_id: str
    client_secret: str
    redirect_uri: URL
    subscription_key: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SkyConfig":
        return structure(data, cls)

    @classmethod
    def from_env(cls) -> "SkyConfig":
        return cls.from_dict(
            {
                "client_id": os.environ[SkyConfigEnvVars.CLIENT_ID.value],
                "client_secret": os.environ[SkyConfigEnvVars.CLIENT_SECRET.value],
                "redirect_uri": os.environ[SkyConfigEnvVars.REDIRECT_URI.value],
                "subscription_key": os.environ[SkyConfigEnvVars.SUBSCRIPTION_KEY.value],
            }
        )

    @classmethod
    def from_json_file(cls, path: Path) -> "SkyConfig":
        return cls.from_dict(json.loads(Path(path).read_text()))

    @classmethod
    def from_stored_config(cls) -> "SkyConfig":
        return cls.from_json_file(BBSKY_CONFIG_FILE)

    def to_dict(self) -> dict[str, Any]:
        return unstructure(self)

    def to_json_file(self, path: Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=4))

    @classmethod
    def load(cls, input_file: Optional[Path] = None):
        f"""
        Loading Priority:

        1. Provided JSON file path
        2. Environment variables
        3. JSON file (default: {BBSKY_CONFIG_FILE})

        """
        if input_file:
            return cls.from_json_file(input_file)
        elif SkyConfigEnvVars.are_all_env_vars_set():
            return cls.from_env()
        elif BBSKY_CONFIG_FILE.exists():
            return cls.from_stored_config()
        else:
            raise SkyConfigError("No config found. Please provide a file path or set environment variables.")


@click.group()
def cli():
    """Create and manage Blackbaud Sky API config."""
    pass


@click.command()
@click.option("--client-id", prompt="Client ID")
@click.option("--client-secret", prompt="Client Secret")
@click.option("--redirect-uri", prompt="Redirect URI")
@click.option("--subscription-key", prompt="Subscription Key")
@click.option("--output-path", type=click.Path(), default=BBSKY_CONFIG_FILE)
@click.pass_context
@ensure_config_dir
def create(
    context: click.Context,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    subscription_key: str,
    output_path: Path,
) -> None:
    """Create a new Blackbaud Sky API config."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    config = SkyConfig(client_id, client_secret, URL(redirect_uri), subscription_key)
    config.to_json_file(output_path)
    click.echo(f"Config saved to {output_path}")


@click.command()
@click.option("-i", "--input_path", type=click.Path(), default=BBSKY_CONFIG_FILE)
@click.option("-f", "--fmt", type=click.Choice(["json", "env"]), default="json")
@click.pass_context
def show(
    context: click.Context,
    input_path: Path,
    fmt: str,
) -> None:
    """Show the current Blackbaud Sky API config."""
    input_path = Path(input_path)
    if not input_path.exists():
        click.echo(f"Config not found at {input_path}.")
        return
    config = SkyConfig.from_json_file(input_path)
    _show(config, fmt)


def _show(config: SkyConfig, fmt: str) -> None:
    """Show the current Blackbaud Sky API config.

    Format options:
    - json: JSON format
    - env: Environment variables

    """
    if fmt == "json":
        click.echo(json.dumps(config.to_dict(), indent=4))
    elif fmt == "env":
        click.echo(f"export {SkyConfigEnvVars.CLIENT_ID.value}={config.client_id}")
        click.echo(f"export {SkyConfigEnvVars.CLIENT_SECRET.value}={config.client_secret}")
        click.echo(f"export {SkyConfigEnvVars.REDIRECT_URI.value}={config.redirect_uri}")
        click.echo(f"export {SkyConfigEnvVars.SUBSCRIPTION_KEY.value}={config.subscription_key}")


@click.command()
@click.option("-i", "--input_path", type=click.Path(), default=BBSKY_CONFIG_FILE)
@click.option("--client-id", prompt="Client ID (leave blank to keep current value)", default="")
@click.option("--client-secret", prompt="Client Secret (leave blank to keep current value)", default="")
@click.option("--redirect-uri", prompt="Redirect URI (leave blank to keep current value)", default="")
@click.option("--subscription-key", prompt="Subscription Key (leave blank to keep current value)", default="")
@click.pass_context
@ensure_config_dir
def update(
    context: click.Context,
    input_path: Path,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    subscription_key: str,
) -> None:
    """Update the current Blackbaud Sky API config."""

    if not any([client_id, client_secret, redirect_uri, subscription_key]):
        click.echo("No new values provided. Exiting.")
        return

    # Load the original config
    input_path = Path(input_path)
    input_path.parent.mkdir(parents=True, exist_ok=True)
    config_orig = SkyConfig.from_json_file(input_path)

    # Show the original config
    click.echo("\nCurrent SkyConfig:")
    _show(config_orig, "json")

    # Update with new values
    config_updated = evolve(
        config_orig,
        **{
            "client_id": client_id if client_id else config_orig.client_id,
            "client_secret": client_secret if client_secret else config_orig.client_secret,
            "redirect_uri": URL(redirect_uri) if redirect_uri else config_orig.redirect_uri,
            "subscription_key": subscription_key if subscription_key else config_orig.subscription_key,
        },
    )

    # Show the updated config
    click.echo("\nUpdated SkyConfig:")
    _show(config_updated, "json")

    # Confirm user wants to save the updated config
    if click.confirm("Save the updated config?"):
        config_updated.to_json_file(input_path)
        click.echo(f"Config updated and saved to {input_path}")
    else:
        click.echo("Config not saved.")


@click.command()
@click.option("-i", "--input_path", type=click.Path(), default=BBSKY_CONFIG_FILE)
@click.pass_context
def purge(
    context: click.Context,
    input_path: Path,
) -> None:
    """Delete the current Blackbaud Sky API config."""
    input_path = Path(input_path)
    if click.confirm(f"Are you sure you want to delete the current config '{input_path}'?"):
        if input_path.exists():
            input_path.unlink()
            click.echo(f"Config deleted at {input_path}")
        else:
            click.echo(f"Config not found at {input_path}. Nothing to delete.")
    else:
        click.echo("Aborted.")


cli.add_command(create)
cli.add_command(show)
cli.add_command(update)
cli.add_command(purge)
