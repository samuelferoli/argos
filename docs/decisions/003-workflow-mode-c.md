# 003. Workflow mode C: Claude does plumbing, Samuel codes the AI parts

- **Status:** Accepted
- **Date:** 2026-10-28
- **Issue:** #2

## Context

The project exists to learn. If Claude writes everything, nothing is learned. If Samuel
writes everything, setup and boilerplate slow the project down too much.

## Options

1. **Claude writes everything, Samuel reads** — fastest, least learning.
2. **Samuel writes everything, Claude reviews** — most learning, much slower.
3. **Split by kind of work** — Claude does plumbing; Samuel does the AI-specific parts.

## Decision

Option 3. Claude handles setup, configuration, I/O, OAuth boilerplate and
documentation. Samuel writes the AI-specific code: prompts, tool definitions, the agent
loop and memory injection.

The loop for Samuel's parts, through pull requests:

1. Claude provides a skeleton with `TODO`s.
2. Samuel codes it and opens a PR.
3. Claude reviews and gives feedback.
4. Samuel revises, and Claude reviews again.
5. Claude writes the final, correct version.

Issues carry the labels `owner: samuel` and `owner: claude`.

## Consequences

- Learning stays on the parts that matter.
- Each of Samuel's issues takes more rounds than if Claude wrote it.
- Claude must not write the AI-core code before Samuel has tried it.
