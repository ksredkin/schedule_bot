class ChangesCache:
    _instance = None
    changes = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.changes = []
        return cls._instance

    def get(self) -> list|None:
        return self.changes

    def set(self, changes: dict):
        self.changes = changes