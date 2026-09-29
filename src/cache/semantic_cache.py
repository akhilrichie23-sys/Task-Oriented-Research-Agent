import hashlib
from diskcache import Cache

class SemanticCache:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache = Cache(cache_dir)

    def _generate_key(self, prompt: str, model_name: str) -> str:
        raw_str = f"{model_name}:{prompt.strip().lower()}"
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

    def get(self, prompt: str, model_name: str):
        key = self._generate_key(prompt, model_name)
        return self.cache.get(key)

    def set(self, prompt: str, model_name: str, response: str, expire_seconds: int = 86400):
        key = self._generate_key(prompt, model_name)
        self.cache.set(key, response, expire=expire_seconds)
