"""Tests for core.transaction_model — Transaction status flow."""

from core.transaction_model import Transaction


def test_transaction_creation_defaults():
    t = Transaction("TXN001", "P001", "B001", "R001", 50000)
    assert t.status == "PENDING"
    assert t.delivery_id is None
    assert t.amount == 50000


def test_next_status_sequential():
    t = Transaction("TXN001", "P001", "B001", "R001", 50000)
    assert t.next_status() == "PAID"
    t.status = "PAID"
    assert t.next_status() == "SHIPPED"
    t.status = "SHIPPED"
    assert t.next_status() == "DELIVERED"
    t.status = "DELIVERED"
    assert t.next_status() == "REFUNDED"


def test_next_status_at_end_returns_none():
    t = Transaction("TXN001", "P001", "B001", "R001", 50000)
    t.status = "REFUNDED"
    assert t.next_status() is None


def test_next_status_unknown_status():
    t = Transaction("TXN001", "P001", "B001", "R001", 50000)
    t.status = "UNKNOWN"
    assert t.next_status() is None


def test_to_dict_roundtrip():
    t = Transaction("TXN001", "P001", "B001", "R001", 50000, "PAID")
    t.delivery_id = "D001"
    d = t.to_dict()
    restored = Transaction.from_dict(d)
    assert restored.txn_id == "TXN001"
    assert restored.status == "PAID"
    assert restored.delivery_id == "D001"


def test_from_dict_default_status():
    d = {"txn_id": "TXN001", "product_id": "P001",
         "buyer_id": "B001", "retailer_id": "R001",
         "amount": 50000}
    t = Transaction.from_dict(d)
    assert t.status == "PENDING"
    assert t.delivery_id is None
