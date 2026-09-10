"""Tests for retailer/buyer CLI menus."""

import pytest
from core.models import User, Product


def test_buyer_menu_logout(patched_db, capsys, monkeypatch):
    from cli.buyer_menu import buyer_menu
    from services.auth import AuthManager
    auth = AuthManager()
    buyer = User("B001", "Buyer", "buyer", "p", "BUYER")
    auth.current_user = buyer
    monkeypatch.setattr("builtins.input", lambda _: "6")
    buyer_menu(auth)
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_buyer_menu_view_products_label(patched_db, capsys, monkeypatch):
    from cli.buyer_menu import buyer_menu
    from services.auth import AuthManager
    auth = AuthManager()
    buyer = User("B001", "Buyer", "buyer", "p", "BUYER")
    auth.current_user = buyer
    monkeypatch.setattr("builtins.input", lambda _: "6")
    buyer_menu(auth)
    out = capsys.readouterr().out
    assert "View Products" in out


def test_retailer_menu_logout(patched_db, capsys, monkeypatch):
    from cli.retailer_menu import retailer_menu
    from services.auth import AuthManager
    auth = AuthManager()
    retailer = User("R001", "Store", "store", "p", "RETAILER")
    auth.current_user = retailer
    monkeypatch.setattr("builtins.input", lambda _: "4")
    retailer_menu(auth)
    out = capsys.readouterr().out
    assert "Goodbye" in out


def test_retailer_mark_ready_label(patched_db, capsys, monkeypatch):
    """Retailer menu shows 'Mark Ready for Delivery'."""
    from cli.retailer_menu import retailer_menu
    from services.auth import AuthManager
    auth = AuthManager()
    retailer = User("R001", "Store", "store", "p", "RETAILER")
    auth.current_user = retailer
    monkeypatch.setattr("builtins.input", lambda _: "4")
    retailer_menu(auth)
    out = capsys.readouterr().out
    assert "Mark Ready for Delivery" in out