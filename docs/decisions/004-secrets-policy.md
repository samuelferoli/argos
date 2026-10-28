# 004. Secrets policy

- **Status:** Accepted
- **Date:** 2026-10-28
- **Issue:** #2

## Context

The repository is **public**. Argos will use an LLM API key and, later, tokens for
Notion, GitHub, TickTick and Google Calendar. Development happens on a work computer
and a personal one, and the work computer may have policies about personal accounts.

## Options

1. **Keys in the code or committed config** — never acceptable in a public repo.
2. **Keys in a gitignored `.env` file** — simple and standard, but the keys sit on disk
   as plain text.
3. **OS keychain through the `keyring` library** — uses Windows Credential Manager on
   Windows and the Secret Service (GNOME Keyring) on Linux Mint. Free, no account, no
   server, encrypted by the OS. Needs a running keyring service on Linux.
4. **A cloud secrets manager (Bitwarden Secrets Manager, Infisical, Doppler, ...)** —
   central and shareable, but needs an account, may have free-tier limits, and stores
   the tokens on a third party's servers. More than a one-person project needs.

## Decision

- No secret is ever committed.
- Secrets are stored in the **OS keychain via `keyring`**. A small `secrets` module is
  the only place that reads them, so the rest of the code never knows where they come
  from.
- **Lookup order:** environment variable first, then the keychain. The environment
  override keeps things working where no keychain exists (CI, a headless server).
- Environment variables may be loaded from a gitignored `.env` as a fallback. `.env` is
  in `.gitignore`, and the repo contains only `.env.example` with placeholders.
- Personal tokens (Notion, GitHub, TickTick, Calendar) may be used on the work computer,
  at Samuel's discretion, with these guardrails:
  - least privilege: the smallest scopes that work, read-only first;
  - every token is revocable and revoked when the work computer is returned or
    replaced;
  - nothing is stored in the work computer's shared or synced locations.
  The keychain protects against leaks in the repo, not against the employer's IT
  monitoring or policies; those remain Samuel's responsibility.
- If a secret is ever committed by mistake, treat it as leaked: revoke it first, then
  clean up the history.

## Consequences

- Safe for a public repo, with no plain-text keys on disk in the normal case.
- Works on both Windows and Linux Mint, with no cost and no account.
- Setup needs a one-time step per secret (for example `argos secrets set LLM_API_KEY`),
  which becomes part of the skeleton in #4.
- On Linux Mint the keyring daemon must be running (it is by default on Cinnamon); to
  be checked when setting up the personal machine.
- Features that need personal tokens (Phases 4–5) can be developed on either machine.
- Revisit a cloud secrets manager if Argos ever runs on a server or is shared.
