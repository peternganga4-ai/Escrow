"""Tests for services.transaction_service — Create, find, list."""

from core.models import User, Product
from services.transaction_service import (
    create_transaction, find_transaction, list_transactions_by_user,
    advance_transaction,
)


def _setup_buyer_and_product(patched_db):
    buyer = User("B001", "Buyer", "buyer", "p", "BUYER", 200000)
    retailer = User("R001", "Store", "store", "p", "RETAILER")
    product = Product("P001", "Laptop", 85000, "R001", "Nice", 10)
    patched_db.save("users", [buyer.to_dict(), retailer.to_dict()])
    patched_db.save("products", [product.to_dict()])
    return buyer, retailer, product

def test_create_transaction_success(patched_db, capsys):
    buyer, _, _ = _setup_buyer_and_product(patched_db)
    txn = create_transaction("P001", buyer)
    assert txn is not None
    assert txn.status == "PENDING"
    assert txn.amount == 85000


def test_create_insufficient_balance(patched_db, capsys):
    buyer = User("B001", "Poor", "poor", "p", "BUYER", 1000)
    retailer = User("R001", "Store", "store", "p", "RETAILER")
    product = Product("P001", "Laptop", 85000, "R001", "Nice", 10)
    patched_db.save("users", [buyer.to_dict(), retailer.to_dict()])
    patched_db.save("products", [product.to_dict()])
    txn = create_transaction("P001", buyer)
    assert txn is None



def test_find_transaction(patched_db, capsys):
    buyer, _, _ = _setup_buyer_and_product(patched_db)
    txn = create_transaction("P001", buyer)
    found = find_transaction(txn.txn_id)
    assert found is not None
    assert found.txn_id == txn.txn_id


def test_list_transactions_by_user(patched_db, capsys):
    buyer, _, _ = _setup_buyer_and_product(patched_db)
    create_transaction("P001", buyer)
    txns = list_transactions_by_user("B001")
    assert len(txns) == 1


def test_delivery_sees_shipped(patched_db, capsys):
    """Delivery agents see SHIPPED txns even if not assigned."""
    from core.models import User
    from services.transaction_service import advance_transaction
    buyer, _, _ = _setup_buyer_and_product(patched_db)
    txn = create_transaction("P001", buyer)
    advance_transaction(txn.txn_id, buyer)  # → PAID (sets delivery_code)
    retailer = User("R001", "Store", "store", "p", "RETAILER")
    advance_transaction(txn.txn_id, retailer)  # → SHIPPED
    txns = list_transactions_by_user("D001", role="DELIVERY")
    assert len(txns) == 1
    assert txns[0].status == "SHIPPED"

