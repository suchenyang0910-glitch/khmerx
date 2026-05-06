from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, Header, HTTPException

from app import config


@dataclass
class AdminPrincipal:
    username: str


def _require_admin_jwt_secret():
    if not config.ADMIN_JWT_SECRET:
        raise HTTPException(status_code=500, detail="ADMIN_JWT_SECRET not configured")


def issue_admin_token(username: str, ttl_hours: int = 24) -> str:
    _require_admin_jwt_secret()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=ttl_hours)).timestamp()),
        "scope": "admin",
    }
    return jwt.encode(payload, config.ADMIN_JWT_SECRET, algorithm="HS256")


def get_current_admin(authorization: str | None = Header(None)) -> AdminPrincipal:
    _require_admin_jwt_secret()
    if not authorization:
        raise HTTPException(status_code=401, detail="missing authorization")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="invalid authorization")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, config.ADMIN_JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")
    if payload.get("scope") != "admin":
        raise HTTPException(status_code=403, detail="admin scope required")
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="invalid token")
    return AdminPrincipal(username=str(sub))


AdminDep = Depends(get_current_admin)
