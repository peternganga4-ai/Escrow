"""Tests for advance_transaction."""
import pytest
from core.models import User, Product
from core.transaction_model import Transaction
from services.transaction_service import advance_transaction, find_transaction


def _setup_full_flow(patched_db):
    buyer = User("B001", "Buyer", "buyer", "p", "BUYER", 200000)
    retailer = User("R001", "Store", "store", "p", "RETAILER", 0)
    driver = User("D001", "Deliver", "driver", "p", "DELIVERY")
    trustee = User("T001", "Trust", "trust", "p", "TRUSTEE")
    product = Product("P001", "Laptop", 85000, "R001", "Nice", 9)
    patched_db.save("users", [buyer.to_dict(), retailer.to_dict(),
                              driver.to_dict(), trustee.to_dict()])
    patched_db.save("products", [product.to_dict()])
    txn = Transaction("TXN001", "P001", "B001", "R001", 85000)
    patched_db.save("transactions", [txn.to_dict()])
    return buyer, retailer, txn


def _pay_and_ship(patched_db):
    buyer, retailer, txn = _setup_full_flow(patched_db)
    advance_transaction(txn.txn_id, buyer)
    advance_transaction(txn.txn_id, retailer)
    return buyer, retailer, find_transaction("TXN001")


def test_advance_to_paid_by_buyer(patched_db, capsys):
    buyer, _, txn = _setup_full_flow(patched_db)
    advance_transaction(txn.txn_id, buyer)
    assert "PAID" in capsys.readouterr().out


def test_wrong_delivery_code_rejected(patched_db, capsys):
    _, _, txn = _pay_and_ship(patched_db)
    driver = User("D001", "Deliver", "driver", "p", "DELIVERY")
    result = advance_transaction(txn.txn_id, driver, "000000")
    assert "Invalid" in capsys.readouterr().out or result is None


def test_no_code_delivered_rejected(patched_db, capsys):
    _, _, txn = _pay_and_ship(patched_db)
    driver = User("D001", "Deliver", "driver", "p", "DELIVERY")
    result = advance_transaction(txn.txn_id, driver, None)
    assert "Invalid" in capsys.readouterr().out or result is None


def test_no_refund_after_release(patched_db, capsys):
    buyer, _, txn = _pay_and_ship(patched_db)
    driver = User("D001", "Deliver", "driver", "p", "DELIVERY")
    advance_transaction(txn.txn_id, driver, txn.delivery_code)
    txn = find_transaction("TXN001")
    result = advance_transaction(txn.txn_id, buyer)
    assert "Cannot refund" in capsys.readouterr().out or result is None
