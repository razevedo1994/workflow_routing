# Research Summarizer

A conversational backend built with Python and the Anthropic Claude API. Users submit a topic, URL, or PDF and interact in natural language; a central router classifies the intent and dispatches to the specialized agent that handles it, which then uses tools to fetch, parse, and reason over content.

This project is a standalone learning ground for workflow routing patterns — multi-agent orchestration, tool use, dependency injection, and stateful memory — with no dependency on any other side project or agent framework (no LangChain/LangGraph).

## Status

Early scaffold. The routing schema (`schemas/router/routing.py`) is implemented; most modules under `core/`, `services/`, `agents/`, and `tools/` are stubs being filled in incrementally. See [`CLAUDE.md`](./CLAUDE.md) for the full architecture, build phases, and design principles.

## Architecture

```
workflow_routing/
├── core/
│   ├── router.py            # intent classification → agent selection
│   ├── workflow.py          # multi-step flow orchestration
│   └── state.py             # conversation history & shared context
│
├── services/
│   ├── api/claude_client.py # Anthropic SDK wrapper (injected via DI)
│   └── memory/              # short-term session state & long-term retrieval
│
├── agents/                  # domain reasoning agents (summarizer, critic, ...)
├── tools/                   # pure functions: web fetch, PDF parsing, etc.
├── prompts/                 # system prompt templates per agent
├── schemas/
│   └── router/routing.py    # Pydantic I/O models, e.g. RoutingDecision
├── config/
│   ├── settings.py          # env vars, model name, token limits
│   ├── middleware.py        # guardrails, rate limiting, budget caps
│   └── observability.py     # token usage, latency, structured traces
└── main.py                  # CLI / HTTP entry point
```

## Request flow

```
user input
    │
    ▼
core/router.py     ← classifies intent using the Claude API
    │
    ▼
agent selection    ← summarizer | critic | comparison | extractor
    │
    ▼
tool calls         ← web_fetch | pdf_reader | search | citation_parser
    │
    ▼
structured response
```

## Stack

| Layer | Choice |
|---|---|
| Language | Python 3.12+ |
| LLM | Anthropic Claude API |
| Validation | Pydantic v2 |
| Dependency management | uv + pyproject.toml |

## Setup

```bash
uv sync
```

Configure environment variables (see `config/settings.py`):

```bash
ANTHROPIC_API_KEY=sk-...
```

Run:

```bash
uv run main.py
```

## Design principles

- **Dependency injection** — `Router` and each agent receive their dependencies (e.g. `ClaudeClient`) via constructor, never via global imports.
- **Layered separation of concerns** — `services/` holds external integrations only; `core/` holds routing/orchestration logic with no direct SDK calls; `agents/` holds domain reasoning, independently testable; `tools/` holds pure functions with no routing awareness.
- **No agent framework dependency** — routing and memory are implemented directly in plain Python/Pydantic rather than via LangChain, LangGraph, or similar.

Full details, the intent → agent mapping, build phases, and testing strategy live in [`CLAUDE.md`](./CLAUDE.md).
