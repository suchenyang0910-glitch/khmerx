from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ApiError(Exception):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    status_code: int = 400

