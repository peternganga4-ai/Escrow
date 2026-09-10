"""Tests for services.delivery_code — Code generation and verification."""

from core.transaction_model import Transaction
from services.delivery_code import generate_delivery_code, verify_delivery_code

def test_generate_code_format():
    code = generate_delivery_code()
    assert len(code) == 6
    assert code.isdigit()


def test_generate_code_uniqueness():
    codes = {generate_delivery_code() for _ in range(20)}
    assert len(codes) > 1
def test_verify_correct_code():
    txn = Transaction("TXN001", "P001", "B001", "R001", 50000, "PAID")
    txn.delivery_code = "654321"
    assert verify_delivery_code(txn, "654321") is True
def test_verify_wrong_code():
    txn = Transaction("TXN001", "P001", "B001", "R001", 50000, "PAID")
    txn.delivery_code = "654321"
    assert verify_delivery_code(txn, "000000") is False

def test_verify_no_code_on_txn():
    txn = Transaction("TXN001", "P001", "B001", "R001", 50000)
    assert txn.delivery_code is None
    assert verify_delivery_code(txn, "123456") is False


def test_verify_none_code_input():
    txn = Transaction("TXN001", "P001", "B001", "R001", 50000, "PAID")
    txn.delivery_code = "123456"
    assert verify_delivery_code(txn, None) is False         