# Argos

> A simple, free personal assistant — one conversation and one useful tool at a time.

**Status:** Phase 0 — planning and setup ([board](https://github.com/users/samuelferoli/projects/1))

## What is Argos

Argos is a personal assistant I'm building for myself. The goal is twofold: to end up
with a tool I actually use every day, and to learn how LLM agents really work by
building one from the ground up — turning the theory from the AWS AIF-C01 into
practice.

It starts small: a conversation, one tool, a little memory. Everything else grows from there.

## V1 scope

- A conversation interface (terminal first)
- A free hosted model behind a swappable interface
- One or a few useful tools
- Only explicitly allowed commands, with confirmation before sensitive actions
- Simple memory

**Exit criterion:**

> Talk, run one authorized tool, and recall a preference — with no required recurring cost.

V1 is complete at the end of Phase 3.

## Roadmap

| Phase | What gets built | AI concept learned |
|---|---|---|
| 0 | Send one message to an LLM API | Tokens, system prompt, temperature, limits |
| 1 | Terminal chat with history | Context window; why the model "forgets" |
| 2 | Memory of preferences (SQLite) | In-context learning vs. fine-tuning |
| 3 | First tool + agent loop, written by hand | Tool/function calling |
| 4 | GitHub and Notion, read-only | Tool design; putting data into prompts |
| 5 | TickTick and Calendar → "what's my day?" briefing | OAuth; combining several tools |
| 6 | Goals → metrics, project health | Reasoning over data; prompt engineering |
| Later | "Knows all my context" | Embeddings and RAG |
| Later | Write actions, scheduled briefings, voice, MCP | Agents, safety, automation |

Phase 0 is tracked in [its milestone](https://github.com/samuelferoli/argos/milestone/1);
later phases get a milestone when they start.

## Principles and limits

- **Side project.** It only moves forward when there is room. It must not compete
  with my main projects or my studies.
- **Free by default.** No required recurring cost.
- **Read-only first.** Anything that changes something asks for confirmation.
- **No secrets in the repo.** It is public; keys live in a gitignored `.env`.
- **Hand-written agent loop.** No framework at first — the loop is the thing to learn.

The reasoning behind each choice will be recorded as decision records (see Docs).

## Future (not now)

Possibilities only — no implementation or commitment: voice, alerts, agenda, e-mail,
automations, authorized control of other apps, a "Life OS", devices, and calls.

The integrations planned after V1 are Notion, GitHub, TickTick and Google Calendar.

## How we work

- Claude handles the plumbing and documentation.
- I write the AI-specific code: prompts, tools, the agent loop, memory.
- Every change goes through a pull request: I code, Claude reviews, I revise, and
  then Claude writes the final version.

Work is tracked in [issues](https://github.com/samuelferoli/argos/issues) and on the
[project board](https://github.com/users/samuelferoli/projects/1).

## Getting started

Argos is a Python project managed with [uv](https://docs.astral.sh/uv/), which also
installs the right Python version for you.

**1. Install uv**

- Windows (PowerShell): `winget install --id astral-sh.uv` (or see the uv docs)
- Linux Mint: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**2. Get the code and install dependencies**

```
git clone https://github.com/samuelferoli/argos.git
cd argos
uv sync
```

**3. Run it**

```
uv run argos
```

**Secrets** (such as the LLM API key) live in your OS keychain, not in files:

```
uv run argos secrets set LLM_API_KEY
uv run argos secrets status
```

On Linux Mint this uses the system keyring (GNOME Keyring), which is normally running by
default on the desktop. Non-secret settings can go in a `.env` file; copy `.env.example`.

**Development**

```
uv run pytest        # tests
uv run ruff check .  # lint
uv run ruff format . # format
```

The setup has been run on Windows; the Linux Mint steps have not been tested yet.

## Docs

- [Decision records](docs/decisions/README.md)
- Learning notes — coming soon (#6)
