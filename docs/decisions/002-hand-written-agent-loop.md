# 002. Hand-written agent loop, no framework

- **Status:** Accepted
- **Date:** 2026-10-28
- **Issue:** #2

## Context

A big goal of Argos is to learn how LLM agents actually work. The core of an agent is a
loop: send the conversation to the model, see whether it asks to call a tool, run the
tool, feed the result back, and repeat. Frameworks such as LangChain wrap this loop.

## Options

1. **A framework (LangChain, etc.)** — faster to a working demo, but the loop and the
   prompts are hidden behind abstractions, and the APIs change often.
2. **The provider's SDK only, loop written by hand** — more code to write, but every
   step is visible.

## Decision

Write the agent loop by hand on top of the provider's SDK or plain HTTP calls. No agent
framework in V1.

## Consequences

- Samuel writes and understands each step of tool calling (Phase 3).
- Fewer dependencies and less churn.
- More code to maintain; features a framework gives for free must be built if needed.
- Revisit after V1: a framework may make sense once the mechanics are well understood.
