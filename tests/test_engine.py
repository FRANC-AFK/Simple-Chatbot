import pytest
from chatbot.engine import get_response

def test_hours_query():
    """Test that hours queries return appropriate responses."""
    response = get_response("What time are you open?")
    assert "9 AM to 5 PM" in response["reply"]
    assert response["type"] in ["rule", "ai", "cached"]

def test_hours_query_alternative():
    """Test alternative phrasing for hours."""
    response = get_response("When are you open?")
    assert response["type"] in ["rule", "ai", "cached"]
    assert len(response["reply"]) > 0

def test_price_query():
    """Test that price queries return appropriate responses."""
    response = get_response("How much does it cost?")
    assert "free" in response["reply"].lower()
    assert response["type"] in ["rule", "ai", "cached"]

def test_contact_query():
    """Test contact information queries."""
    response = get_response("How can I contact you?")
    assert response["type"] in ["rule", "ai", "cached"]
    assert len(response["reply"]) > 0

def test_location_query():
    """Test location queries."""
    response = get_response("Where are you located?")
    assert response["type"] in ["rule", "ai", "cached"]
    assert len(response["reply"]) > 0

def test_fallback():
    """Test that unrecognized queries return fallback."""
    response = get_response("What is the meaning of life?")
    assert response["type"] == "fallback"
    assert "can only help" in response["reply"]

def test_empty_message():
    """Test empty message handling."""
    response = get_response("")
    assert response["type"] == "fallback"

def test_response_structure():
    """Test that responses have the correct structure."""
    response = get_response("What are your hours?")
    assert isinstance(response, dict)
    assert "reply" in response
    assert "type" in response
    assert isinstance(response["reply"], str)
    assert isinstance(response["type"], str)
