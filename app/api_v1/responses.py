from __future__ import annotations

from typing import Any, Dict, Optional


def ok(data: Any = None, message: str = "success") -> Dict[str, Any]:
    return {
        "ok": True,
        "data": {} if data is None else data,
        "message": message,
    }


def fail(code: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "ok": False,
        "error": {
            "code": code,
            "message": message,
            "details": {} if details is None else details,
        },
    }

