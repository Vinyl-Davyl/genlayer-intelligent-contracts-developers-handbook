"""
Direct mode tests for the Hello contract.
Run with: pytest tests/test_hello.py -v
"""
import pytest


def test_greet_returns_formatted_name(direct_deploy):
    """Contract should return greeting with the deployed name."""
    contract = direct_deploy("contracts/hello.py", ["World"])
    result = contract.greet()
    assert result == "Hello, World!"


def test_set_name_updates_greeting(direct_deploy):
    """Setting a new name should update the greeting output."""
    contract = direct_deploy("contracts/hello.py", ["World"])
    contract.set_name("GenLayer")
    assert contract.greet() == "Hello, GenLayer!"


def test_empty_name(direct_deploy):
    """Contract should handle empty string names."""
    contract = direct_deploy("contracts/hello.py", [""])
    assert contract.greet() == "Hello, !"


def test_unicode_name(direct_deploy):
    """Contract should handle unicode characters in names."""
    contract = direct_deploy("contracts/hello.py", ["GenLayer"])
    assert contract.greet() == "Hello, GenLayer!"
