# tests/test_generator.py

import pytest
from bohancompliment import (
    compliment,
    personalized_compliment,
    multi_compliment,
    compliment_in_language,
)

def test_compliment():
    result = compliment("Alice")
    assert "Alice" in result

def test_personalized_compliment():
    result = personalized_compliment("Alice", "creativity")
    assert "Alice" in result and "creativity" in result

def test_multi_compliment():
    results = multi_compliment("Alice", 3)
    assert len(results) == 3
    assert all("Alice" in res for res in results)

def test_compliment_in_language_supported():
    result = compliment_in_language("Bob", "es")
    assert "Bob" in result and "¡Eres increíble" in result

def test_compliment_in_language_unsupported():
    result = compliment_in_language("Charlie", "de")
    assert "not supported" in result
