from typing import Any, List, Dict

def serialize_response(data: Any):
    """
    Converts asyncpg Record(s) to dict(s) for FastAPI responses.
    """
    if data is None:
        return None

    # Single row (asyncpg.Record)
    if hasattr(data, "keys"):
        return dict(data)

    # Multiple rows (list of Records)
    if isinstance(data, list):
        return [dict(row) for row in data]

    # Fallback (already serializable)
    return data
