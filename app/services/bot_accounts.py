from __future__ import annotations

from typing import Iterable, List, Optional

from sqlalchemy.orm import Session

from app.models.bot_account import BotAccount


def get_active_bot(db: Session) -> Optional[BotAccount]:
    bot = (
        db.query(BotAccount)
        .filter(BotAccount.is_primary.is_(True), BotAccount.status == "active")
        .first()
    )
    if bot:
        return bot

    return db.query(BotAccount).filter(BotAccount.status == "active").first()


def get_active_bot_tokens(db: Session) -> List[str]:
    bots: Iterable[BotAccount] = (
        db.query(BotAccount)
        .filter(BotAccount.status == "active")
        .order_by(BotAccount.is_primary.desc(), BotAccount.id.asc())
        .all()
    )
    return [b.bot_token for b in bots if b.bot_token]

