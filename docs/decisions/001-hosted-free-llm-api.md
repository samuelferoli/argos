# 001. Hosted free LLM API instead of a local model

- **Status:** Accepted
- **Date:** 2026-10-28
- **Issue:** #2

## Context

Argos should give good responses and good tool use at no recurring cost. The machines
available are a work PC (16 GB RAM, integrated graphics, no dedicated GPU) and a
personal Linux Mint machine that is weaker. Running a model locally means a small model
on the CPU, which is slow and gives weaker answers.

## Options

1. **Local model (e.g. via Ollama)** — free and private, but small models only,
   slow, and noticeably worse at tool calling on this hardware.
2. **Hosted API, free tier** — strong models and fast, but subject to rate limits and
   to the provider's data-use terms.
3. **Hosted API, paid** — best quality, but conflicts with the no-cost requirement.

## Decision

Use a **hosted API on a free tier**. Argos talks to the model through one small
interface, so changing provider (or adding a local backend later) means changing a
config value, not the rest of the code. The specific provider is chosen in a separate
record (#3).

## Consequences

- Good answers and tool calling without hardware or cost.
- Free tiers have request and token limits; the code must handle rate-limit errors.
- Prompts leave the machine. Provider data-use terms must be checked before choosing
  one, because Argos will see tasks, notes and calendar data.
- A local backend stays possible later behind the same interface.
