import pytest
from chatbot.cache import ResponseCache

def test_cache_set_and_get():
    """Test basic cache set and get operations."""
    cache = ResponseCache(max_size=5)
    
    cache.set("hello", "hi there")
    result = cache.get("hello")
    
    assert result == "hi there"

def test_cache_case_insensitive():
    """Test that cache is case-insensitive."""
    cache = ResponseCache()
    
    cache.set("Hello World", "response")
    result = cache.get("hello world")
    
    assert result == "response"

def test_cache_miss():
    """Test cache miss returns None."""
    cache = ResponseCache()
    
    result = cache.get("nonexistent")
    
    assert result is None

def test_cache_max_size():
    """Test that cache respects max size."""
    cache = ResponseCache(max_size=2)
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")  # Should evict key1
    
    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"
    assert cache.size() == 2

def test_cache_clear():
    """Test cache clear operation."""
    cache = ResponseCache()
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()
    
    assert cache.size() == 0
    assert cache.get("key1") is None
