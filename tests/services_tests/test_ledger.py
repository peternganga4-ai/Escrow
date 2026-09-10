"""Tests for services.ledger — Ledger entry utilities."""

from services.ledger import add_ledger_entry


def test_add_ledger_entry_basic(patched_db):
    add_ledger_entry("TXN001", "HOLD", 50000, from_id="B001")
    ledger = patched_db.load("ledger")
    assert len(ledger) == 1
    assert ledger[0]["txn_id"] == "TXN001"
    assert ledger[0]["type"] == "HOLD"
    assert ledger[0]["amount"] == 50000
    assert ledger[0]["from"] == "B001"

