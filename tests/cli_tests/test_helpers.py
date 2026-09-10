"""Tests for cli.helpers — Input and display utilities."""

from cli.helpers import show_transaction, show_balance
from core.transaction_model import Transaction
from core.models import User


def test_show_transaction_output(capsys):
    txn = Transaction("TXN001", "P001", "B001", "R001", 85000, "PAID")
    txn.delivery_id = "D001"
    show_transaction(txn)
    out = capsys.readouterr().out
    assert "TXN001" in out and "PAID" in out and "85,000" in out


def test_show_transaction_shipped_displays_ready(capsys):
    txn = Transaction("TXN002", "P001", "B001", "R001", 5000, "SHIPPED")
    show_transaction(txn)
    out = capsys.readouterr().out
    assert "READY FOR DELIVERY" in out and "SHIPPED" not in out


def test_show_transaction_buyer_sees_code(capsys):
    txn = Transaction("TXN001", "P001", "B001", "R001", 85000, "PAID")
    txn.delivery_code = "123456"
    show_transaction(txn, viewer_role="BUYER")
    assert "123456" in capsys.readouterr().out


def test_show_transaction_non_buyer_no_code(capsys):
    txn = Transaction("TXN001", "P001", "B001", "R001", 85000, "PAID")
    txn.delivery_code = "123456"
    show_transaction(txn, viewer_role="DELIVERY")
    assert "123456" not in capsys.readouterr().out


def test_show_transaction_no_delivery(capsys):
    txn = Transaction("TXN002", "P002", "B002", "R002", 5000)
    show_transaction(txn)
    out = capsys.readouterr().out
    assert "TXN002" in out and "Delivery" not in out


def test_show_balance(capsys):
    user = User("B001", "John", "john", "p", "BUYER", 100000)
    user.locked = 30000
    show_balance(user)
    out = capsys.readouterr().out
    assert "100,000" in out and "30,000" in out


def test_show_balance_no_locked(capsys):
    user = User("R001", "Store", "store", "p", "RETAILER")
    show_balance(user)
    assert "Locked" not in capsys.readouterr().out


def test_prompt_choice_valid(monkeypatch, capsys):
    from cli.helpers import prompt_choice
    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert prompt_choice("Pick", ["A", "B", "C"]) == "A"


def test_prompt_choice_invalid(monkeypatch, capsys):
    from cli.helpers import prompt_choice
    monkeypatch.setattr("builtins.input", lambda _: "99")
    assert prompt_choice("Pick", ["A", "B"]) is None


def test_confirm_yes(monkeypatch):
    from cli.helpers import confirm
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert confirm("Continue?") is True


def test_confirm_no(monkeypatch):
    from cli.helpers import confirm
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert confirm("Continue?") is False