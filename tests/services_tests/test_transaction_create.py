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
