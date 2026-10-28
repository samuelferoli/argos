# 005. LLM provider: Groq (free tier)

- **Status:** Accepted
- **Date:** 2026-10-28
- **Issue:** #3

## Context

[ADR-001](001-hosted-free-llm-api.md) chose a hosted free LLM API. Argos will send
tasks, notes and calendar data to it, so what the provider does with prompts matters as
much as quality. Candidates were compared in
[issue #3](https://github.com/samuelferoli/argos/issues/3#issuecomment-6477795085)
using the providers' own documentation where possible.

## Options

1. **Groq** — tool calling on all hosted models. Its docs say inference data is not
   retained by default, and any customer can enable Zero Data Retention (ZDR). Tight
   tokens-per-minute limit.
2. **Gemini API** — on the free tier Google uses prompts to improve its products, human
   reviewers may read them, and its terms say not to submit personal information.
   Rejected for privacy.
3. **OpenRouter free models** — 50 requests per day without purchased credits; too
   small for an agent, where every tool call is a request. Provider data policies vary.
4. **Mistral (Experiment plan)** — generous limits, but reportedly trains on data unless
   opted out (not verified from Mistral's own docs). Kept as the backup.
5. **GitHub Models** — fully retired on 2026-07-30.

## Decision

Use **Groq on its free tier, with Zero Data Retention enabled**. Start with
`openai/gpt-oss-120b` and fall back to `llama-3.3-70b-versatile`. Mistral is the planned
alternative if Groq's limits get in the way.

Argos reaches the model through one interface (ADR-001), so the provider and model
names live in configuration, not in the code.

## Consequences

- Prompts leave the machine, but Groq's docs say inference data is not retained by
  default. With ZDR on, reliability and abuse logs are not kept either.
- Tool calling is available, which Phase 3 needs.
- Free-plan limits are tight, especially tokens per minute (8K on the table verified at
  the time). Prompts and history must stay small, and the code must handle rate-limit
  errors (HTTP 429) with a clear message and a retry.
- Free-tier terms change often. Limits and terms must be re-checked in the account
  console, not trusted from this record.

## To verify (tracked in #5)

- The exact free-plan limits shown in the Groq console.
- That ZDR is enabled on the account.
- That the Services Agreement bars training on inputs; only a third-party quote of it
  was found.
- The OpenAI-compatible endpoint (`/docs/openai`) works as expected.
