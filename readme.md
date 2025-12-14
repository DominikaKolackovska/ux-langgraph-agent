# UX LangGraph Agent (LangChain + LangGraph)

A lightweight UX troubleshooting agent built with LangChain and LangGraph.
The agent uses OpenAI for reasoning and tool-calling, and optionally queries a Supabase Postgres database containing real UX research issues.

The goal of this project is to demonstrate a hybrid agent architecture:
- database-first retrieval (RAG-style)
- deterministic heuristic fallback
- LLM-based reasoning and response synthesis

---

## Features

- Tool-based agent loop (ReAct-style) implemented with LangGraph
- Tools:
  - `search_ux_db(query)`  
    Queries a Supabase Postgres table `ux_issues` for similar UX problems
  - `ux_heuristics(query)`  
    Deterministic UX heuristics analysis (severity, risks, recommendations)
- Database-first decision flow with automatic fallback to heuristics
- Human-readable UX explanations (no raw JSON output)
- CLI chat interface for quick testing in VS Code

---

## Project Structure

```text
app/
  agent.py        # LangGraph agent definition
  db.py           # Postgres / Supabase database access
  tools.py        # Agent tools (DB search, heuristics)
  prompts.py      # System prompt and agent instructions
  main.py         # CLI entry point
