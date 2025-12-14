from __future__ import annotations

from langchain_core.messages import HumanMessage
from .agent import build_graph
from .config import settings


def main():
    if not settings.openai_api_key:
        raise RuntimeError("Missing OPENAI_API_KEY. Create a .env file from .env.example.")

    app = build_graph()

    print("UX LangGraph Agent (type 'exit' to quit)")
    print("DB enabled:", settings.has_db())
    print("-" * 60)

    state = {"messages": []}

    while True:
        user = input("\nYou: ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        if not user:
            print("Please type a UX issue (or 'exit' to quit).")
            continue

        state["messages"].append(HumanMessage(content=user))
        out = app.invoke(state)
        state = out

        last = out["messages"][-1]
        print("\nAgent:", last.content)


if __name__ == "__main__":
    main()
