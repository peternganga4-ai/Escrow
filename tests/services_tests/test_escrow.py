"""Tests for services.escrow — Fund release and refund with fees."""

from core.models import User, Product
from core.transaction_model import Transaction
from services.user_service import find_user_by_id
from services.escrow import release_funds, refund_funds


def _setup_escrow(patched_db):
    buyer = User("B001", "Buyer", "buyer", "p", "BUYER", 115000)
    buyer.locked = 85000
    retailer = User("R001", "Store", "store", "p", "RETAILER")
    driver = User("D001", "Deliver", "driver", "p", "DELIVERY")
    trustee = User("T001", "Trust", "trust", "p", "TRUSTEE")
    product = Product("P001", "Laptop", 85000, "R001", "Nice", 9)
    patched_db.save("users", [buyer.to_dict(), retailer.to_dict(),
                              driver.to_dict(), trustee.to_dict()])
    patched_db.save("products", [product.to_dict()])
    txn = Transaction("TXN001", "P001", "B001", "R001", 85000, "DELIVERED")
    txn.delivery_id = "D001"
    patched_db.save("transactions", [txn.to_dict()])
    return txn


def test_release_funds_with_fees(patched_db):
    txn = _setup_escrow(patched_db)
    release_funds(txn)
    retailer = find_user_by_id("R001")
    driver = find_user_by_id("D001")
    trustee = find_user_by_id("T001")
    buyer = find_user_by_id("B001")
    assert retailer.balance == 81600
    assert driver.balance == 2550
    assert trustee.balance == 850
    assert buyer.locked == 0


def test_refund_funds(patched_db):
    txn = _setup_escrow(patched_db)
    refund_funds(txn)
    buyer = find_user_by_id("B001")
    assert buyer.balance == 200000
    assert buyer.locked == 0
    from services.product_service import find_product
    assert find_product("P001").stock == 10


def test_release_adds_ledger_entries(patched_db):
    txn = _setup_escrow(patched_db)
    release_funds(txn)
    ledger = patched_db.load("ledger")
    assert len(ledger) == 3
    types = {e["type"] for e in ledger}
    assert types == {"RELEASE", "DELIVERY_FEE", "TRUSTEE_FEE"}


def test_refund_adds_ledger_entry(patched_db):
    txn = _setup_escrow(patched_db)
    refund_funds(txn)
    ledger = patched_db.load("ledger")
    assert len(ledger) == 1
    assert ledger[0]["type"] == "REFUND"