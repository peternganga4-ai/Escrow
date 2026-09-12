import random


def generate_delivery_code():
    return f"{random.randint(100000, 999999)}"


def verify_delivery_code(txn, code):
    if not txn.delivery_code:
        return False
    return str(code).strip() == str(txn.delivery_code)
