# Math Agent

A simple agent built using Google ADK that answers math questions using MCP tools.

## Prerequisites

- [Deno](https://docs.deno.com/runtime/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

1.  **Install dependencies:**
    ```bash
    uv sync -U
    ```
2.  **Configure environment:**
    Copy `src/.env.example` to `src/.env` and fill in your API keys.

## Running the Agent

```bash
uv -m src.math_agent.agent
```
