# 00. LLM API basics

Notes to read before writing your first call in [#7](https://github.com/samuelferoli/argos/issues/7).
They connect what AIF-C01 covered in theory to what you will actually type.

Details here come from Groq's docs (checked 2026-10-28). Where something is not
confirmed, it says so. Anything marked **Try it** is something to see for yourself in #7
and #8.

## 1. What an LLM API call is

A call is one HTTP request and one response. You send text in a structured form; the
model sends text back. That is all an "AI assistant" is at the lowest level.

For Groq, the request goes to:

```
POST https://api.groq.com/openai/v1/chat/completions
Authorization: Bearer <your API key>
```

The `/openai/v1/` part is not an accident. Groq copies the shape of OpenAI's API, which
many providers also copy. That is why switching provider later (ADR-001) is mostly
changing a base URL, a key and a model name.

The request body looks like this:

```json
{
  "model": "openai/gpt-oss-120b",
  "messages": [
    {"role": "system", "content": "You are Argos, a concise personal assistant."},
    {"role": "user", "content": "What is a token?"}
  ],
  "temperature": 0.7,
  "max_completion_tokens": 300
}
```

And the response, trimmed:

```json
{
  "choices": [
    {
      "message": {"role": "assistant", "content": "A token is a chunk of text..."},
      "finish_reason": "stop"
    }
  ],
  "usage": {"prompt_tokens": 42, "completion_tokens": 118, "total_tokens": 160}
}
```

(The numbers are made up; the field names are Groq's.)

**Roles.** Every message has a `role`:

| Role | Who writes it | Purpose |
|---|---|---|
| `system` | You, the developer | Instructions that set behaviour and personality |
| `user` | The person talking | The question or request |
| `assistant` | The model | Its earlier replies |
| `tool` | Your code (Phase 3) | The result of a tool the model asked to run |

**The most important idea: the API is stateless.** The model remembers nothing between
calls. If you want a conversation, *you* resend the whole history inside `messages` every
time. A "chat" is just a list that your code keeps appending to. Hold on to this; it
explains the context window (section 6) and the token limits (section 2).

*AIF-C01 link:* this is the "inference" step of a foundation model. On AWS Bedrock the
equivalent calls are `InvokeModel` and `Converse`.

## 2. Tokens

A model does not read letters or words. It reads **tokens**: chunks of text, roughly a
short word or part of a longer one. Rough rule of thumb for English: 1 token is about 4
characters, or about three-quarters of a word. Portuguese usually needs *more* tokens for
the same meaning, because the tokenizers are built mostly around English.

Tokens matter for three reasons:

1. **Limits.** Groq's free plan allows 8K tokens per minute and 200K per day for our
   models (ADR-005). Input and output both count.
2. **Cost.** Paid APIs charge per token. We are on a free tier, but the habit is the
   same: tokens are the unit of cost.
3. **Memory.** The model can only look at so many tokens at once (section 6).

The response tells you exactly what you used, in `usage`:

- `prompt_tokens`: everything you sent (system prompt + history + your message)
- `completion_tokens`: what the model wrote
- `total_tokens`: the sum

You control the output side with `max_completion_tokens` (the older name `max_tokens` is
deprecated). A cap on output protects your token budget.

**Try it (#8):** send a one-word question and a long paragraph, and compare
`prompt_tokens`. Then ask the same question in English and in Portuguese.

*AIF-C01 link:* tokens, and the "response length" inference parameter.

## 3. The system prompt

The `system` message is where Argos gets its personality and rules. The model treats it
as standing instructions for the whole conversation.

```
You are Argos, a personal assistant for Samuel. Be concise. Answer in the language the
user writes in. If you are not sure, say so instead of guessing.
```

Good system prompts are short, specific and testable. Things worth putting in one: who
the assistant is, tone, language rules, what it must never do, and the format of answers.

Two honest limits:

- It is **guidance, not a guarantee.** A model can still ignore or misread it. Never rely
  on the system prompt alone to protect something sensitive; that is why Argos will also
  check permissions in code (ADR-003, and later phases).
- It **costs tokens on every single call**, because of the stateless point above. A
  500-token system prompt is 500 tokens of your 8K minute, each time.

**Try it (#8):** write two very different system prompts (a formal butler, a sarcastic
pirate) and ask the same question.

*AIF-C01 link:* prompt engineering, and the "system prompt" technique.

## 4. Temperature and top-p

The model produces text one token at a time. At each step it computes a probability for
every possible next token, then **samples** one. These two settings shape that sampling.

- **`temperature`** (0 to 2 on Groq, default 1): low values make the model pick the most
  likely token almost every time, so answers are consistent and predictable. High values
  flatten the odds, so answers are more varied and more likely to drift.
- **`top_p`** (0 to 1, default 1): only consider the smallest group of tokens whose
  probabilities add up to `top_p`. Lower means a narrower, safer choice.

Rule of thumb: change **one** of them, not both. For Argos:

| Task | Temperature |
|---|---|
| Tool calls, extracting facts, briefings | low (0 to 0.3) |
| Casual chat | around 0.7 |
| Brainstorming | 1 or higher |

Notes from Groq's docs: a temperature of 0 is silently converted to a tiny positive
number (1e-8), and even at 0 the output is *nearly* repeatable, not guaranteed identical.
Groq's docs list no `top_k`, which AIF-C01 also mentions; it is just not offered here.

**Try it (#8):** ask the same question three times at temperature 0 and three times at 1.
How different are the answers?

*AIF-C01 link:* inference parameters (temperature, top P, top K).

## 5. Rate limits and errors

Free tiers protect themselves with limits. Ours (ADR-005): 30 requests per minute, 1,000
per day, 8K tokens per minute, 200K per day.

When you go over, the API refuses the call with an HTTP error instead of answering. The
one to know is **429 Too Many Requests**, which means "slow down". Other families you
will meet:

| Status | Usually means | What to do |
|---|---|---|
| 400 | Your request is malformed or uses an unsupported value | Fix the request; retrying will not help |
| 401 | Missing or wrong API key | Check the key |
| 429 | Over a rate limit | Wait, then retry |
| 5xx | The provider has a problem | Retry later |

The right way to handle a 429 is to **wait and retry**, and to show a clear message
instead of a crash. Do not retry in a tight loop; that makes it worse.

I did not find Groq's retry hint headers in the docs I checked. When you trigger a 429 on
purpose in #8, look at the response headers and see what it gives you.

## 6. The context window (preview of Phase 1)

The **context window** is the maximum number of tokens a model can consider in one call:
system prompt, the whole history, your new message *and* its answer, all together.

Because the API is stateless, a long conversation means resending a longer and longer
`messages` list. That has two consequences you will feel in Phase 1:

1. Past a point it no longer fits and something has to be dropped or summarized.
2. Long before that, every call spends more of your 8K tokens-per-minute budget.

This is also why "memory" in an assistant is not magic: it is deciding *what to put back
into the prompt* each time. Phase 1 (history) and Phase 2 (preferences) are both about
that choice. I have not checked the context size of `gpt-oss-120b`; we will look it up
when it matters.

*AIF-C01 link:* context window, and why retrieval (RAG) exists at all: it fetches only
the relevant pieces instead of stuffing everything in.

## Summary

| Concept | One line |
|---|---|
| API call | One HTTP request in, one response out |
| Stateless | The model forgets; you resend the history each call |
| Roles | system (rules), user (you), assistant (model), tool (Phase 3) |
| Tokens | The unit of limits, cost and memory; shown in `usage` |
| System prompt | Standing instructions; guidance, not a guarantee |
| Temperature | Low = consistent, high = varied |
| 429 | Slow down: wait and retry |
| Context window | How much the model can see at once |

## Questions

Add your questions as comments on
[#6](https://github.com/samuelferoli/argos/issues/6); I will answer them and fold the
good ones back into this file.

## My experiments

*(Filled in during [#8](https://github.com/samuelferoli/argos/issues/8).)*
