import core.database as db

import core.database as db


def add_ledger_entry(txn_id, entry_type, amount, from_id=None, to_id=None):
    ledger = db.load("ledger")
    entry = {
        "txn_id": txn_id,
        "type": entry_type,
        "amount": amount,
    }
    if from_id:
        entry["from"] = from_id
    if to_id:
        entry["to"] = to_id
    ledger.append(entry)
    db.save("ledger", ledger)
