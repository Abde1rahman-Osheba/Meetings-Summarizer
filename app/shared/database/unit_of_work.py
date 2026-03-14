class UnitOfWork:
    """Placeholder unit of work abstraction."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def commit(self) -> None:
        return None

    def rollback(self) -> None:
        return None
