import json
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

from bbsky.config import SkyConfig, SkyConfigError
from bbsky.data_cls import URL


@pytest.fixture
def valid_credentials_dict() -> dict[str, str]:
    return {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret",
        "redirect_uri": "https://example.com/callback",
        "subscription_key": "sk-1234",
    }


@pytest.fixture
def valid_credentials(valid_credentials_dict: dict[str, str]) -> SkyConfig:
    return SkyConfig.from_dict(valid_credentials_dict)


def test_app_credentials_from_dict(valid_credentials_dict: dict[str, str], valid_credentials: SkyConfig):
    assert valid_credentials.client_id == valid_credentials_dict["client_id"]
    assert valid_credentials.client_secret == valid_credentials_dict["client_secret"]
    assert valid_credentials.redirect_uri == URL(valid_credentials_dict["redirect_uri"])
    assert valid_credentials.subscription_key == valid_credentials_dict["subscription_key"]


def test_app_credentials_to_dict(valid_credentials: SkyConfig, valid_credentials_dict: dict[str, str]):
    result = valid_credentials.to_dict()
    assert result["client_id"] == valid_credentials_dict["client_id"]
    assert result["client_secret"] == valid_credentials_dict["client_secret"]
    assert result["redirect_uri"] == valid_credentials_dict["redirect_uri"]
    assert result["subscription_key"] == valid_credentials_dict["subscription_key"]


def test_app_credentials_from_env(monkeypatch: MonkeyPatch, valid_credentials_dict: dict[str, str]) -> None:
    monkeypatch.setenv("BLACKBAUD_CLIENT_ID", valid_credentials_dict["client_id"])
    monkeypatch.setenv("BLACKBAUD_CLIENT_SECRET", valid_credentials_dict["client_secret"])
    monkeypatch.setenv("BLACKBAUD_REDIRECT_URI", valid_credentials_dict["redirect_uri"])
    monkeypatch.setenv("BLACKBAUD_SUBSCRIPTION_KEY", valid_credentials_dict["subscription_key"])

    credentials = SkyConfig.from_env()
    assert credentials.client_id == valid_credentials_dict["client_id"]
    assert credentials.client_secret == valid_credentials_dict["client_secret"]
    assert credentials.redirect_uri == URL(valid_credentials_dict["redirect_uri"])
    assert credentials.subscription_key == valid_credentials_dict["subscription_key"]


def test_app_credentials_from_json_file(tmp_path: Path, valid_credentials_dict: dict[str, str]) -> None:
    json_file = tmp_path / "credentials.json"
    json_file.write_text(json.dumps(valid_credentials_dict))

    credentials: SkyConfig = SkyConfig.from_json_file(json_file)
    assert credentials.client_id == valid_credentials_dict["client_id"]
    assert credentials.client_secret == valid_credentials_dict["client_secret"]
    assert credentials.redirect_uri == URL(valid_credentials_dict["redirect_uri"])
    assert credentials.subscription_key == valid_credentials_dict["subscription_key"]


def test_app_credentials_to_json_file(tmp_path: Path, valid_credentials: SkyConfig) -> None:
    json_file = tmp_path / "credentials.json"
    valid_credentials.to_json_file(json_file)
    assert json_file.exists()


def test_app_credentials_from_env_missing_env_var(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("BLACKBAUD_CLIENT_ID", raising=False)
    monkeypatch.setenv("BLACKBAUD_CLIENT_SECRET", "test_secret")
    monkeypatch.setenv("BLACKBAUD_REDIRECT_URI", "https://example.com/callback")
    monkeypatch.setenv("BLACKBAUD_SUBSCRIPTION_KEY", "sk-1234")

    with pytest.raises(KeyError):
        SkyConfig.from_env()


def test_app_credentials_from_json_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        SkyConfig.from_json_file(Path("non_existent_file.json"))


def test_app_credentials_from_json_file_invalid_json(tmp_path: Path) -> None:
    invalid_json_file = tmp_path / "invalid.json"
    invalid_json_file.write_text("{ invalid json }")

    with pytest.raises(json.JSONDecodeError):
        SkyConfig.from_json_file(invalid_json_file)


def test_stored_config_from_json_file(
    tmp_path: Path, monkeypatch: MonkeyPatch, valid_credentials_dict: dict[str, str]
) -> None:
    json_file = tmp_path / "credentials.json"
    json_file.write_text(json.dumps(valid_credentials_dict))

    monkeypatch.setattr("bbsky.config.BBSKY_CONFIG_FILE", json_file)
    credentials: SkyConfig = SkyConfig.from_stored_config()
    assert credentials.client_id == valid_credentials_dict["client_id"]
    assert credentials.client_secret == valid_credentials_dict["client_secret"]
    assert credentials.redirect_uri == URL(valid_credentials_dict["redirect_uri"])
    assert credentials.subscription_key == valid_credentials_dict["subscription_key"]


def test_stored_config_file_not_found(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("bbsky.config.BBSKY_CONFIG_FILE", Path("non_existent_file.json"))
    with pytest.raises(FileNotFoundError):
        SkyConfig.from_stored_config()


def test_stored_config_invalid_json(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    invalid_json_file = tmp_path / "invalid.json"
    invalid_json_file.write_text("{ invalid json }")

    monkeypatch.setattr("bbsky.config.BBSKY_CONFIG_FILE", invalid_json_file)
    with pytest.raises(json.JSONDecodeError):
        SkyConfig.from_stored_config()


def load_config_from_provided_file(tmp_path: Path, valid_credentials_dict: dict[str, str]) -> None:
    json_file = tmp_path / "credentials.json"
    json_file.write_text(json.dumps(valid_credentials_dict))

    config = SkyConfig.load(input_file=json_file)
    assert config.client_id == valid_credentials_dict["client_id"]
    assert config.client_secret == valid_credentials_dict["client_secret"]
    assert config.redirect_uri == URL(valid_credentials_dict["redirect_uri"])
    assert config.subscription_key == valid_credentials_dict["subscription_key"]


def load_config_from_env(monkeypatch: MonkeyPatch, valid_credentials_dict: dict[str, str]) -> None:
    monkeypatch.setenv("BLACKBAUD_CLIENT_ID", valid_credentials_dict["client_id"])
    monkeypatch.setenv("BLACKBAUD_CLIENT_SECRET", valid_credentials_dict["client_secret"])
    monkeypatch.setenv("BLACKBAUD_REDIRECT_URI", valid_credentials_dict["redirect_uri"])
    monkeypatch.setenv("BLACKBAUD_SUBSCRIPTION_KEY", valid_credentials_dict["subscription_key"])

    config = SkyConfig.load()
    assert config.client_id == valid_credentials_dict["client_id"]
    assert config.client_secret == valid_credentials_dict["client_secret"]
    assert config.redirect_uri == URL(valid_credentials_dict["redirect_uri"])
    assert config.subscription_key == valid_credentials_dict["subscription_key"]


def load_config_from_stored_file(
    tmp_path: Path, monkeypatch: MonkeyPatch, valid_credentials_dict: dict[str, str]
) -> None:
    json_file = tmp_path / "credentials.json"
    json_file.write_text(json.dumps(valid_credentials_dict))
    monkeypatch.setattr("bbsky.config.BBSKY_CONFIG_FILE", json_file)

    config = SkyConfig.load()
    assert config.client_id == valid_credentials_dict["client_id"]
    assert config.client_secret == valid_credentials_dict["client_secret"]
    assert config.redirect_uri == URL(valid_credentials_dict["redirect_uri"])
    assert config.subscription_key == valid_credentials_dict["subscription_key"]


def load_config_no_sources(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("BLACKBAUD_CLIENT_ID", raising=False)
    monkeypatch.delenv("BLACKBAUD_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("BLACKBAUD_REDIRECT_URI", raising=False)
    monkeypatch.delenv("BLACKBAUD_SUBSCRIPTION_KEY", raising=False)
    monkeypatch.setattr("bbsky.config.BBSKY_CONFIG_FILE", Path("non_existent_file.json"))

    with pytest.raises(SkyConfigError):
        SkyConfig.load()
