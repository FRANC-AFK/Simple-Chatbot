import pytest
from chatbot.rate_limiter import RateLimiter
import time

def test_rate_limiter_allows_requests():
    """Test that rate limiter allows requests within limit."""
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    
    # Should allow 5 requests
    for i in range(5):
        assert limiter.is_allowed("test_user") is True

def test_rate_limiter_blocks_excess():
    """Test that rate limiter blocks requests exceeding limit."""
    limiter = RateLimiter(max_requests=3, window_seconds=60)
    
    # Allow 3 requests
    for i in range(3):
        assert limiter.is_allowed("test_user") is True
    
    # Block 4th request
    assert limiter.is_allowed("test_user") is False

def test_rate_limiter_separate_users():
    """Test that rate limiter tracks users separately."""
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    
    assert limiter.is_allowed("user1") is True
    assert limiter.is_allowed("user2") is True
    assert limiter.is_allowed("user1") is True
    assert limiter.is_allowed("user2") is True
    
    # Both users hit limit
    assert limiter.is_allowed("user1") is False
    assert limiter.is_allowed("user2") is False

def test_rate_limiter_window_expiry():
    """Test that rate limiter window expires correctly."""
    limiter = RateLimiter(max_requests=2, window_seconds=1)
    
    # Use up quota
    assert limiter.is_allowed("test_user") is True
    assert limiter.is_allowed("test_user") is True
    assert limiter.is_allowed("test_user") is False
    
    # Wait for window to expire
    time.sleep(1.1)
    
    # Should allow again
    assert limiter.is_allowed("test_user") is True

def test_rate_limiter_get_remaining():
    """Test getting remaining request count."""
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    
    assert limiter.get_remaining("test_user") == 5
    
    limiter.is_allowed("test_user")
    assert limiter.get_remaining("test_user") == 4
    
    limiter.is_allowed("test_user")
    assert limiter.get_remaining("test_user") == 3

def test_rate_limiter_reset():
    """Test resetting rate limit for a user."""
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    
    limiter.is_allowed("test_user")
    limiter.is_allowed("test_user")
    assert limiter.is_allowed("test_user") is False
    
    limiter.reset("test_user")
    assert limiter.is_allowed("test_user") is True
