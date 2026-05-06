"""KhmerX 数据库引擎 & Session"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine, event, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import TypeDecorator, TEXT, CHAR
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

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


def get_engine():
    global _engine
    if _engine is not None:
        return _engine

    is_sqlite = "sqlite" in DATABASE_URL
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    engine = create_engine(DATABASE_URL, connect_args=connect_args)

    if is_sqlite:
        @event.listens_for(engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    _engine = engine
    return _engine


def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


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
    import app.risk.models
    import app.ops.models
    Base.metadata.create_all(bind=get_engine())

    engine = get_engine()
    if "sqlite" in str(engine.url):
        from sqlalchemy import inspect, text

        insp = inspect(engine)
        if "users" in insp.get_table_names():
            cols = {c["name"] for c in insp.get_columns("users")}
            if "phone_verified_at" not in cols:
                with engine.begin() as conn:
                    conn.execute(text("ALTER TABLE users ADD COLUMN phone_verified_at DATETIME"))

    from app.models.interest_rate import InterestRateMatrix
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
