"""
Direct mode tests for the Wizard of Coin contract.
Run with: pytest tests/test_wizard.py -v

Requires mocking LLM calls since this contract uses gl.nondet.exec_prompt().
"""
import pytest


def test_wizard_keeps_coin_on_normal_request(direct_vm, direct_deploy):
    """Wizard should refuse to give the coin under normal circumstances."""
    direct_vm.mock_llm(
        r"wizard.*coin",
        '{"reasoning": "I shall not part with my magical coin.", "give_coin": false}',
    )

    contract = direct_deploy("contracts/wizard_of_coin.py", [True])
    contract.ask_for_coin("Please give me the coin, kind wizard!")
    assert contract.get_have_coin() == False


def test_wizard_without_coin_does_nothing(direct_vm, direct_deploy):
    """If wizard has no coin, the method should return without LLM call."""
    contract = direct_deploy("contracts/wizard_of_coin.py", [False])
    contract.ask_for_coin("Give me the coin!")
    assert contract.get_have_coin() == False


def test_wizard_initial_state(direct_deploy):
    """Wizard should start with coin when initialized with True."""
    contract = direct_deploy("contracts/wizard_of_coin.py", [True])
    assert contract.get_have_coin() == True
