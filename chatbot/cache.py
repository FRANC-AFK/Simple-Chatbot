import hashlib
from typing import Optional

class ResponseCache:
    """Simple in-memory cache for chatbot responses."""
    
    def __init__(self, max_size: int = 100):
        self._cache = {}
        self._max_size = max_size
    
    def get_key(self, text: str) -> str:
        """Generate a cache key from the input text."""
        return hashlib.md5(text.lower().strip().encode()).hexdigest()
    
    def get(self, text: str) -> Optional[str]:
        """Retrieve cached response if it exists."""
        return self._cache.get(self.get_key(text))
    
    def set(self, text: str, response: str):
        """Store a response in the cache."""
        if len(self._cache) >= self._max_size:
            # Remove oldest entry (first item in dict)
            self._cache.pop(next(iter(self._cache)))
        self._cache[self.get_key(text)] = response
    
    def clear(self):
        """Clear all cached responses."""
        self._cache.clear()
    
    def size(self) -> int:
        """Return the current cache size."""
        return len(self._cache)

response_cache = ResponseCache()
