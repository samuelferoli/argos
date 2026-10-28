# 004. Secrets policy

- **Status:** Proposed
- **Date:** 2026-10-28
- **Issue:** #2

## Context

The repository is **public**. Argos will use an LLM API key and, later, tokens for
Notion, GitHub, TickTick and Google Calendar. Development happens on a work computer
and a personal one, and the work computer may have policies about personal accounts.

## Options

1. **Keys in the code or committed config** — never acceptable in a public repo.
2. **Keys in a gitignored `.env` file** — simple, standard, works on both operating
   systems.
3. **A secrets manager or OS keychain** — safer, but more setup than V1 needs.

## Decision

- No secret is ever committed. Code reads secrets from environment variables, loaded
  from a local `.env` file.
- `.env` is in `.gitignore`. The repo contains only `.env.example` with placeholder
  values.
- Personal tokens (Notion, GitHub, TickTick, Calendar) are **not stored on the work
  computer** unless Samuel has confirmed that his employer's policy allows it.
- If a secret is ever committed by mistake, treat it as leaked: revoke it first, then
  clean up the history.

## Consequences

- Safe for a public repo and easy on both Windows and Linux Mint.
- Features that need personal tokens (Phases 4–5) are developed and run on the
  personal machine unless the work-computer rule is relaxed.
- Keys live as plain text on disk; acceptable for V1, revisit with a keychain later.

## To confirm

Samuel to confirm the work-computer rule before this moves to **Accepted**.
