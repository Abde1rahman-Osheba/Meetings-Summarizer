from collections.abc import Generator


def get_db_session() -> Generator[None, None, None]:
    """Placeholder dependency for SQLAlchemy session."""
    yield None
