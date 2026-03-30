class ImageCache:
    _instance = None
    cache = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.cache = {}
        return cls._instance

    def get(self, image: str) -> dict | None:
        return self.cache.get(image)

    def set(self, image: str, image_id: int):
        if image not in self.cache:
            self.cache[image] = image_id
