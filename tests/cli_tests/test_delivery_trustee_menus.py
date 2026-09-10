"""Tests for delivery and trustee CLI menus."""

import pytest
from core.models import User, Product
from core.transaction_model import Transaction


def _setup_delivery_flow(patched_db):
    buyer = User("B001", "Buyer", "buyer", "p", "BUYER", 115000)
    buyer.locked = 85000
    retailer = User("R001", "Store", "store", "p", "RETAILER")
    driver = User("D001", "Deliver", "driver", "p", "DELIVERY")
    trustee = User("T001", "Trust", "trust", "p", "TRUSTEE")
    product = Product("P001", "Laptop", 85000, "R001", "Nice", 9)
    txn = Transaction("TXN001", "P001", "B001", "R001", 85000, "SHIPPED")
    txn.delivery_code = "288779"
    txn.delivery_id = "D001"
    patched_db.save("users", [buyer.to_dict(), retailer.to_dict(),
                              driver.to_dict(), trustee.to_dict()])
    patched_db.save("products", [product.to_dict()])
    patched_db.save("transactions", [txn.to_dict()])
    return driver


def test_delivery_menu_logout(patched_db, capsys, monkeypatch):
    from cli.delivery_menu import delivery_menu
    from services.auth import AuthManager
    auth = AuthManager()
    driver = _setup_delivery_flow(patched_db)
    auth.current_user = driver
    monkeypatch.setattr("builtins.input", lambda _: "4")
    delivery_menu(auth)
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_trustee_menu_logout(patched_db, capsys, monkeypatch):
    from cli.trustee_menu import trustee_menu
    from services.auth import AuthManager
    auth = AuthManager()
    trustee = User("T001", "Trust", "trust", "p", "TRUSTEE")
    auth.current_user = trustee
    monkeypatch.setattr("builtins.input", lambda _: "4")
    trustee_menu(auth)
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_delivery_available_deliveries(patched_db, capsys, monkeypatch):
    from cli.delivery_menu import delivery_menu
    from services.auth import AuthManager
    auth = AuthManager()
    driver = _setup_delivery_flow(patched_db)
    auth.current_user = driver
    inputs = iter(["1", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delivery_menu(auth)
    out = capsys.readouterr().out
    assert "READY FOR DELIVERY" in out


def test_delivery_confirm_with_code(patched_db, capsys, monkeypatch):
    from cli.delivery_menu import delivery_menu
    from services.auth import AuthManager
    auth = AuthManager()
    driver = _setup_delivery_flow(patched_db)
    auth.current_user = driver
    inputs = iter(["2", "TXN001", "288779", "4"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    delivery_menu(auth)
    out = capsys.readouterr().out
    assert "DELIVERED" in out