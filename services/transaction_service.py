import core.database as db, core.config as config
from core.transaction_model import Transaction
from .user_service import update_user
from .product_service import find_product, save_product
from .escrow import release_funds, refund_funds
from .ledger import add_ledger_entry
from .delivery_code import generate_delivery_code, verify_delivery_code


def _next_txn_id():
    txns = db.load("transactions")
    n = max(
        (
            int(t["txn_id"][3:])
            for t in txns
            if t["txn_id"].startswith("TXN") and t["txn_id"][3:].isdigit()
        ),
        default=0,
    )
    return f"TXN{n + 1:03d}"


def create_transaction(product_id, buyer):
    product = find_product(product_id)
    if not product:
        print("\nProduct not found.")
        return None
    if product.stock <= 0:
        print("\nOut of stock.")
        return None
    if buyer.balance < product.price:
        print("\nInsufficient balance.")
        return None
    txn_id = _next_txn_id()
    txn = Transaction(
        txn_id, product_id, buyer.user_id, product.retailer_id, product.price
    )
    buyer.balance -= product.price
    buyer.locked += product.price
    product.stock -= 1
    update_user(buyer)
    save_product(product)
    txns = db.load("transactions")
    txns.append(txn.to_dict())
    db.save("transactions", txns)
    add_ledger_entry(txn_id, "HOLD", product.price, from_id=buyer.user_id)
    print(f"\nTransaction {txn_id} created. KSh {product.price:,} held.")
    return txn


def advance_transaction(txn_id, user, code=None):
    txn = find_transaction(txn_id)
    if not txn:
        print("\nTransaction not found.")
        return None
    nxt = txn.next_status()
    if not nxt:
        print("\nAlready completed.")
        return None
    if nxt not in config.ROLE_PERMISSIONS.get(user.role, []):
        print(f"\nCannot advance to {nxt}.")
        return None
    if nxt == "REFUNDED" and txn.status in config.NO_REFUND_STATUSES:
        print("\nCannot refund - funds already released.")
        return None
    if nxt == "PAID":
        txn.delivery_code = generate_delivery_code()
    if nxt == "DELIVERED":
        if not verify_delivery_code(txn, code):
            print("\nInvalid delivery code. Get it from the buyer.")
            return None
        txn.delivery_id = user.user_id
    txn.status = nxt
    _save_transaction(txn)
    return _post_advance(txn, nxt, txn_id)


def _post_advance(txn, nxt, txn_id):
    if nxt == "DELIVERED":
        txn.status = "RELEASED"
        _save_transaction(txn)
        release_funds(txn)
        print(f"\n{txn_id} DELIVERED then RELEASED (auto)")
        return txn
    if nxt == "PAID":
        print(
            f"\n{txn_id} PAID | Code: {txn.delivery_code} - share with delivery person!"
        )
        return txn
    if nxt == "REFUNDED":
        refund_funds(txn)
    label = nxt.replace("SHIPPED", "READY FOR DELIVERY")
    print(f"\nTransaction {txn_id}: {label}")
    return txn


def find_transaction(txn_id):
    for t in db.load("transactions"):
        if t["txn_id"] == txn_id:
            return Transaction.from_dict(t)
    return None


def list_transactions_by_user(user_id, role=None):
    txns = db.load("transactions")
    owned = {
        t["txn_id"]
        for t in txns
        if t["buyer_id"] == user_id
        or t["retailer_id"] == user_id
        or t.get("delivery_id") == user_id
    }
    if role == "DELIVERY":
        owned |= {t["txn_id"] for t in txns if t["status"] == "SHIPPED"}
    return [Transaction.from_dict(t) for t in txns if t["txn_id"] in owned]


def _save_transaction(txn):
    txns = db.load("transactions")
    for i, t in enumerate(txns):
        if t["txn_id"] == txn.txn_id:
            txns[i] = txn.to_dict()
            break
    db.save("transactions", txns)
