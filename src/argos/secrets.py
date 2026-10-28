"""The only place that reads or writes secrets (see docs/decisions/004).

Lookup order: environment variable first, then the OS keychain.
"""

import os

import keyring
from keyring.errors import KeyringError, PasswordDeleteError

SERVICE = "argos"


class SecretsError(Exception):
    """The OS keychain is unavailable or refused the request."""


def get_secret(name: str) -> str | None:
    """Return the secret called `name`, or None if it is not set anywhere."""
    value = os.environ.get(name)
    if value:
        return value
    try:
        return keyring.get_password(SERVICE, name)
    except KeyringError as error:
        raise SecretsError(f"Cannot read {name} from the OS keychain: {error}") from error


def set_secret(name: str, value: str) -> None:
    """Store `value` in the OS keychain under `name`."""
    try:
        keyring.set_password(SERVICE, name, value)
    except KeyringError as error:
        raise SecretsError(f"Cannot store {name} in the OS keychain: {error}") from error


def delete_secret(name: str) -> bool:
    """Remove `name` from the OS keychain. Return False if it was not there."""
    try:
        keyring.delete_password(SERVICE, name)
    except PasswordDeleteError:
        return False
    except KeyringError as error:
        raise SecretsError(f"Cannot delete {name} from the OS keychain: {error}") from error
    return True
