import base64
import enum
import hashlib
import logging
import os
import signal
import sys
import threading
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import click
import httpx
from bottle import (  # type: ignore
    LocalRequest,
    Response,
    redirect,  # type: ignore
    request,  # type: ignore
    route,  # type: ignore
    run,  # type: ignore
)  # type: ignore

from bbsky.config import SkyConfig
from bbsky.constants import TOKEN_URL
from bbsky.data_cls import URL
from bbsky.paths import BBSKY_TOKEN_FILE
from bbsky.tokens import OAuth2Token

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

request: LocalRequest

auth_code: str | None = None
oauth_token: OAuth2Token | None = None


# TODO: Make configurable
config = SkyConfig.from_stored_config()


class Scope(enum.Enum):
    """
    Scope for Blackbaud API authentication

    See this URL for more information:
    https://developer.blackbaud.com/skyapi/docs/applications/scopes

    """

    # Add other scopes as needed
    offline_access = "offline_access"


def generate_code_verifier(length: int = 64) -> str:
    return base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8").replace("=", "")


def generate_code_challenge(verifier: str) -> str:
    sha256 = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(sha256).decode("utf-8").replace("=", "")


code_verifier = generate_code_verifier(length=64)
code_challenge = generate_code_challenge(code_verifier)
code_challenge_method = "S256"


def get_random_state() -> str:
    return base64.urlsafe_b64encode(os.urandom(32)).decode().replace("=", "")


def get_state_from_oauth_url(url: URL) -> str | None:
    return url.query.get("state")


def redirect_to_blackbaud(
    client_id: str, redirect_uri: str, scope: str, state: str, code_challenge: str, code_challenge_method: str
) -> Response:
    """Redirect to the Blackbaud authorization URL."""

    # Build up auth params
    # See docs:
    # https://developer.blackbaud.com/skyapi/docs/authorization/auth-code-flow/confidential-application/tutorial
    # TODO: Add in PKCE stuff
    auth_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",  # should always be 'code'
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method,
    }

    auth_request_url = f"https://oauth2.sky.blackbaud.com/authorization?{urlencode(auth_params)}"

    logger.debug(f"Blackbaud Auth Request URL: {auth_request_url}")

    return redirect(auth_request_url)


@route("/")
def home():
    """Home page with a button to login to Blackbaud."""
    return """
    <html>
    <body>
        <form action="/submit" method="post">
            <button type="submit">Login to Blackbaud</button>
        </form>
    </body>
    </html>
    """


@route("/submit", method="POST")
def submit():
    """Redirect to the Blackbaud OAuth2 login flow."""
    return redirect("/login")


@route("/login")
def login_to_blackbaud() -> Response:
    state = get_random_state()
    scope = " ".join([Scope.offline_access.value])
    resp = redirect_to_blackbaud(
        client_id=config.client_id,
        redirect_uri=str(config.redirect_uri),
        scope=scope,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
    )
    return resp


@route("/callback")
def callback_from_blackbaud() -> Response:
    # Step 2: Get the authorization code from the request
    global auth_code
    auth_code = request.GET.get("code")  # type: ignore
    state_echoed = request.GET.get("state")  # type: ignore

    if not auth_code:
        return Response("Authorization code not found in the request.", status=400)

    # Step 3: Exchange the authorization code for an access token
    client_id = config.client_id
    token_params: dict[str, str] = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": str(config.redirect_uri),
        "client_id": client_id,
        "client_secret": config.client_secret,
        "state": state_echoed,
        "code_verifier": code_verifier,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.b64encode(client_id.encode()).decode()}",
    }
    response = httpx.post(str(TOKEN_URL), data=token_params, headers=headers)

    global oauth_token

    if response.status_code == 200:
        logger.info(f"Received access token from Blackbaud. Status code: {response.status_code}")
        oauth_token = OAuth2Token(**response.json())
        logger.debug(f"Access Token: f{str(oauth_token)}")
        return Response("OK", status=200)
    else:
        status_code = response.status_code
        logger.error(f"Error exchanging authorization code for access token. Status code: {status_code}")
        return Response("Error exchanging authorization code for access token", status=status_code)


@route("/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "status_code": 200, "message": "Server is running"}


def run_server(host: str, port: int) -> None:
    run(host=host, port=port, quiet=True)


def start_server(host: str, port: int) -> threading.Thread:
    server_thread = threading.Thread(target=run_server, args=(host, port))
    server_thread.daemon = True
    server_thread.start()
    click.echo(f"Server started on http://{host}:{port}")
    return server_thread


def stop_server(signum: int, frame: Any) -> None:
    click.echo("\nServer stopped.")
    sys.exit(0)


@click.group()
def cli():
    """CLI for Blackbaud OAuth2 server."""
    pass


@click.command()
@click.option("--host", default="localhost", help="Host to bind the server to")
@click.option("--port", default=5000, type=int, help="Port to bind the server to")
@click.option(
    "--token-file", default=BBSKY_TOKEN_FILE, type=str, help="Output filepath to save the token (must be .json)"
)
@click.pass_context
def start(ctx: click.Context, host: str, port: int, token_file: Path) -> None:
    """
    Start the server to listen for OAuth callbacks.
    """
    token_file = Path(token_file)
    if token_file.suffix != ".json":
        raise ValueError("Token file must be a .json file")

    signal.signal(signal.SIGINT, stop_server)

    start_server(host, port)

    click.echo("Waiting for OAuth callback. Press CTRL+C to stop the server.")

    try:
        while True:
            if auth_code and oauth_token:
                click.echo(f"Received authorization code: {auth_code}")

                # Ask if the user wants to save the token
                save_token = click.confirm("Do you want to save the token?")
                if not save_token:
                    break

                # If it exists already, confirm overwrite
                if save_token and token_file.exists():
                    overwrite = click.confirm(f"Token file already exists at {token_file}. Overwrite?")
                    if not overwrite:
                        save_token = False

                if save_token:
                    # Create output path if it doesn't exist
                    token_file.parent.mkdir(parents=True, exist_ok=True)

                    # Save the token
                    oauth_token.save(token_file)
                    click.echo(f"Token saved to {token_file}")

                break

    except KeyboardInterrupt:
        pass

    sys.exit(0)


cli.add_command(start)
