"""BridgeEscrow — Delivery confirmation code utilities."""

import random


def generate_delivery_code():
    """Generate a random 6-digit delivery confirmation code."""
    return f"{random.randint(100000, 999999)}"


def verify_delivery_code(txn, code):
    """Check if the provided code matches the transaction's code."""
    if not txn.delivery_code:
        return False
    return str(code).strip() == str(txn.delivery_code)