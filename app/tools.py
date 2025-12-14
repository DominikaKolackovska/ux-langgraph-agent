from __future__ import annotations

from typing import Any, Dict, List
from langchain_core.tools import tool
from .db import query_similar_ux_issues


@tool
def search_ux_db(query: str) -> List[Dict[str, Any]]:
    """
    Search a UX research database for issues similar to the user's message.
    Input: query (string)
    Output: list of matching UX issues (dicts).
    """
    query = (query or "").strip()
    return query_similar_ux_issues(query, limit=5)


@tool
def ux_heuristics(query: str) -> Dict[str, Any]:
    """
    Run UX heuristic checks on a described problem.
    Returns structured signals (matched heuristics, severity, recommendations).
    """
    text = (query or "").strip().lower()

    heuristics = [
        {
            "id": "visibility_of_system_status",
            "severity": "high",
            "keywords": ["nothing happens", "no feedback", "stuck", "loading", "spinner", "frozen"],
            "risk": "Users are unsure whether their action was registered, causing confusion and drop-off.",
            "recommendation": "Add immediate feedback: loading indicator, disable button on click, show progress and clear error states.",
        },
        {
            "id": "price_transparency",
            "severity": "high",
            "keywords": ["shipping", "delivery", "fees", "total", "price", "cost", "tax"],
            "risk": "Hidden costs reduce trust and increase checkout abandonment.",
            "recommendation": "Show full price breakdown early (items, shipping, tax, fees) and keep it visible throughout checkout.",
        },
        {
            "id": "error_prevention_and_recovery",
            "severity": "high",
            "keywords": ["error", "failed", "doesn't work", "not working", "validation", "required"],
            "risk": "Silent validation and network errors block users without guidance.",
            "recommendation": "Validate inline, show field-level errors, preserve form state, and provide recovery actions.",
        },
        {
            "id": "cta_clarity",
            "severity": "medium",
            "keywords": ["continue", "next", "cta", "button", "submit", "pay"],
            "risk": "Ambiguous CTAs and weak hierarchy prevent users from progressing.",
            "recommendation": "Use clear CTA labels and strong visual hierarchy; place the CTA consistently.",
        },
        {
            "id": "information_hierarchy",
            "severity": "medium",
            "keywords": ["below the fold", "not visible", "hard to find", "hidden", "confusing"],
            "risk": "Critical information is missed due to poor layout and hierarchy.",
            "recommendation": "Move key info above the fold and increase prominence; reduce clutter.",
        },
    ]

    matches = []
    for h in heuristics:
        if any(k in text for k in h["keywords"]):
            matches.append(h)

    return {
        "input": query,
        "matched": matches,
        "summary": [
            {"id": h["id"], "severity": h["severity"], "recommendation": h["recommendation"]}
            for h in matches
        ],
    }
