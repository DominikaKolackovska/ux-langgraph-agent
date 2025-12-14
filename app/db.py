from __future__ import annotations

from typing import Any, List, Dict
from psycopg import connect
from psycopg.rows import dict_row
from .config import settings


def _conn_str() -> str:
    host = settings.supabase_db_host
    port = settings.supabase_db_port
    db = settings.supabase_db_name
    user = settings.supabase_db_user
    pw = settings.supabase_db_password
    return (
        f"host={host} "
        f"port={port} "
        f"dbname={db} "
        f"user={user} "
        f"password={pw} "
        f"sslmode=require"
    )


def _expand_synonyms(user_text: str) -> List[str]:
    """
    Returns a small list of extra keywords to broaden DB search,
    but only when they are relevant to the user input.
    """
    t = (user_text or "").lower()

    synonyms: List[str] = []

    delivery_group = ["delivery", "shipping", "postage", "courier"]
    price_group = ["price", "cost", "fee", "fees", "total", "tax"]

    if any(w in t for w in delivery_group):
        synonyms.extend(["delivery", "shipping"])

    if any(w in t for w in price_group):
        synonyms.extend(["price", "cost", "fee", "total"])

    # remove duplicates while preserving order
    seen = set()
    out: List[str] = []
    for s in synonyms:
        if s not in seen:
            seen.add(s)
            out.append(s)

    return out


def query_similar_ux_issues(user_text: str, limit: int = 5) -> List[Dict[str, Any]]:
    if not settings.has_db():
        print("DB not configured, skipping database lookup")
        return []

    user_text = (user_text or "").strip()
    if len(user_text) < 3:
        print("Empty or too short query, skipping database lookup")
        return []

    print("QUERYING UX DATABASE with:", user_text)

    synonyms = _expand_synonyms(user_text)

    # Build conditions that depend on user input.
    # This avoids returning irrelevant rows for unrelated questions.
    conditions: List[str] = []
    params: List[Any] = []

    # Primary search: user_text across multiple columns
    conditions.append("symptom ilike ('%%' || %s || '%%')")
    params.append(user_text)

    conditions.append("screen ilike ('%%' || %s || '%%')")
    params.append(user_text)

    conditions.append("root_cause ilike ('%%' || %s || '%%')")
    params.append(user_text)

    conditions.append("recommendation ilike ('%%' || %s || '%%')")
    params.append(user_text)

    # Optional synonym broadening: only adds conditions if synonyms exist
    for s in synonyms:
        conditions.append("symptom ilike ('%%' || %s || '%%')")
        params.append(s)

    where_clause = " or ".join(conditions)

    sql = f"""
        select
            product,
            screen,
            symptom,
            root_cause,
            recommendation,
            metric
        from public.ux_issues
        where {where_clause}
        order by created_at desc
        limit %s;
    """

    params.append(limit)

    with connect(_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

    print(f"DB returned {len(rows)} rows")
    return list(rows)
