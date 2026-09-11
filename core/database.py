

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

FILES = {
    "users": os.path.join(DATA_DIR, "users.json"),
    "products": os.path.join(DATA_DIR, "products.json"),
    "transactions": os.path.join(DATA_DIR, "transactions.json"),
    "payments": os.path.join(DATA_DIR, "payments.json"),
    "ledger": os.path.join(DATA_DIR, "ledger.json"),
}


def load(key):
  
    path = FILES[key]
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def save(key, data):

    path = FILES[key]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
