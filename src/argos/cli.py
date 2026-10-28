"""Command line entry point: `argos`."""

import argparse
import getpass
import sys

from argos import __version__
from argos.config import LLM_API_KEY, load_settings
from argos.secrets import SecretsError, delete_secret, get_secret, set_secret

KNOWN_SECRETS = (LLM_API_KEY,)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="argos", description="A simple, free personal assistant.")
    parser.add_argument("--version", action="version", version=f"argos {__version__}")
    commands = parser.add_subparsers(dest="command")

    secrets = commands.add_parser("secrets", help="manage secrets in the OS keychain")
    actions = secrets.add_subparsers(dest="action", required=True)
    for action in ("set", "delete"):
        sub = actions.add_parser(action, help=f"{action} a secret")
        sub.add_argument("name", choices=KNOWN_SECRETS)
    actions.add_parser("status", help="show which secrets are set (never their values)")
    return parser


def run_secrets(action: str, name: str | None) -> int:
    if action == "set":
        value = getpass.getpass(f"Value for {name} (input hidden): ")
        if not value:
            print("Nothing entered; secret not changed.", file=sys.stderr)
            return 1
        set_secret(name, value)
        print(f"{name} stored in the OS keychain.")
    elif action == "delete":
        if delete_secret(name):
            print(f"{name} removed from the OS keychain.")
        else:
            print(f"{name} was not in the OS keychain.")
    else:
        for known in KNOWN_SECRETS:
            state = "set" if get_secret(known) else "not set"
            print(f"{known}: {state}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "secrets":
        try:
            return run_secrets(args.action, getattr(args, "name", None))
        except SecretsError as error:
            print(error, file=sys.stderr)
            return 1

    settings = load_settings()
    print(f"Hello, I'm Argos. (provider: {settings.llm_provider}, model: {settings.llm_model})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
