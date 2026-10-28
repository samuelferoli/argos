import keyring
import pytest
from keyring.backend import KeyringBackend
from keyring.errors import PasswordDeleteError

from argos import secrets


class MemoryKeyring(KeyringBackend):
    """In-memory keychain so tests never touch the real one."""

    priority = 1

    def __init__(self):
        self.items = {}

    def get_password(self, service, username):
        return self.items.get((service, username))

    def set_password(self, service, username, password):
        self.items[(service, username)] = password

    def delete_password(self, service, username):
        try:
            del self.items[(service, username)]
        except KeyError:
            raise PasswordDeleteError("not found") from None


@pytest.fixture(autouse=True)
def memory_keyring(monkeypatch):
    backend = MemoryKeyring()
    keyring.set_keyring(backend)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    return backend


def test_missing_secret_is_none():
    assert secrets.get_secret("LLM_API_KEY") is None


def test_keychain_value_is_returned():
    secrets.set_secret("LLM_API_KEY", "from-keychain")
    assert secrets.get_secret("LLM_API_KEY") == "from-keychain"


def test_environment_overrides_keychain(monkeypatch):
    secrets.set_secret("LLM_API_KEY", "from-keychain")
    monkeypatch.setenv("LLM_API_KEY", "from-env")
    assert secrets.get_secret("LLM_API_KEY") == "from-env"


def test_delete_reports_whether_it_existed():
    secrets.set_secret("LLM_API_KEY", "x")
    assert secrets.delete_secret("LLM_API_KEY") is True
    assert secrets.delete_secret("LLM_API_KEY") is False
