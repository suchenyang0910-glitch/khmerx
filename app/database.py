"""KhmerX 数据库引擎 & Session"""
import sys
import uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine, event, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import TypeDecorator, TEXT, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.pool import StaticPool

from app.config import DATABASE_URL

# ── UUID column helper ───────────────────────────────────────────
class GUID(TypeDecorator):
    """Platform-compatible GUID/UUID column.
    - PostgreSQL: uses native UUID type
    - SQLite: uses TEXT (via CHAR)
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID())
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        u = value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))
        if dialect.name == "postgresql":
            return u
        return u.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(str(value))


# ── Base ─────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


_engine = None
_SessionLocal = None


def _current_module():
    mod = sys.modules.get("app.database")
    return mod if mod is not None else sys.modules[__name__]


def get_engine():
    mod = _current_module()
    if getattr(mod, "_engine", None) is not None:
        return mod._engine

    is_sqlite = "sqlite" in DATABASE_URL
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    use_static_pool = is_sqlite and ":memory:" in DATABASE_URL
    if use_static_pool:
        engine = create_engine(
            DATABASE_URL,
            connect_args=connect_args,
            poolclass=StaticPool,
        )
    else:
        engine = create_engine(DATABASE_URL, connect_args=connect_args)

    if is_sqlite:
        @event.listens_for(engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    mod._engine = engine
    return mod._engine


def get_session_local():
    mod = _current_module()
    if getattr(mod, "_SessionLocal", None) is None:
        mod._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return mod._SessionLocal


def get_db():
    """FastAPI dependency — yields a session."""
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables."""
    import app.models
    from app.models.user import User
    from app.models.interest_rate import InterestRateMatrix
    import app.risk.models
    from app.risk.models import UserRiskProfile
    import app.ops.models
    from app.ops.models import AgentCommission

    engine = get_engine()
    User.metadata.create_all(bind=engine)
    UserRiskProfile.metadata.create_all(bind=engine)
    AgentCommission.metadata.create_all(bind=engine)

    if "sqlite" in str(engine.url):
        from sqlalchemy import inspect, text

        insp = inspect(engine)
        if "users" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("users")}
            if "phone_verified_at" not in cols:
                with engine.begin() as conn:
                    conn.execute(text("ALTER TABLE users ADD COLUMN phone_verified_at DATETIME"))

    from sqlalchemy import inspect

    if "interest_rate_matrix" not in set(inspect(engine).get_table_names()):
        return

    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        existing = db.query(InterestRateMatrix).count()
        if existing == 0:
            defaults = [
                (7, "A", "8.00"),
                (7, "B", "9.00"),
                (7, "C", "10.00"),
                (7, "D", "12.00"),
                (14, "A", "15.00"),
                (14, "B", "17.00"),
                (14, "C", "18.00"),
                (14, "D", "20.00"),
                (30, "A", "25.00"),
                (30, "B", "28.00"),
                (30, "C", "30.00"),
                (30, "D", "35.00"),
            ]
            for term_days, credit_level, rate_percent in defaults:
                db.add(
                    InterestRateMatrix(
                        term_days=term_days,
                        credit_level=credit_level,
                        rate_percent=rate_percent,
                        mode="cut_interest",
                        enabled=True,
                    )
                )
            db.commit()
    finally:
        db.close()
