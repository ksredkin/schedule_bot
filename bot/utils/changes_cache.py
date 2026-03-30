class ChangesCache:
    _instance = None
    changes: list[list[str]] = []

    def __new__(cls) -> ChangesCache:
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.changes = []
        return cls._instance

    def get(self) -> list[list[str]] | None:
        return self.changes

    def set(self, changes: list[list[str]]) -> None:
        self.changes = changes
