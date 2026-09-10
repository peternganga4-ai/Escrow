"""BridgeEscrow — Buyer CLI menu."""

from .helpers import prompt_input, prompt_choice, show_transaction, show_balance
from services.product_service import display_products, find_product
from services.transaction_service import (
    create_transaction, list_transactions_by_user,
    advance_transaction, find_transaction,
)


def buyer_menu(auth):
    """Interactive menu for BUYER users."""
    user = auth.current_user
    while True:
        print(f"\n── Buyer Menu ({user.name}) ──")
        print("  1. View Products")
        print("  2. Purchase Product")
        print("  3. My Transactions")
        print("  4. Pay Transaction")
        print("  5. My Balance")
        print("  6. Logout")
        choice = input("  Choice: ").strip()
        if choice == "1":
            display_products()
        elif choice == "2":
            _purchase_flow(user)
        elif choice == "3":
            _show_my_transactions(user)
        elif choice == "4":
            _pay_flow(user)
        elif choice == "5":
            show_balance(user)
        elif choice == "6":
            auth.logout(); break
        else:
            print("  ✗ Invalid choice.")


def _purchase_flow(user):
    display_products()
    pid = prompt_input("Product ID to purchase")
    if not pid:
        return
    product = find_product(pid)
    if not product:
        print("  ✗ Product not found."); return
    print(f"  Price: KSh {product.price:,} | Stock: {product.stock}")
    if input("  Confirm purchase? (y/n): ").strip().lower() != "y":
        return
    txn = create_transaction(pid, user)
    if txn:
        show_transaction(txn)


def _pay_flow(user):
    _show_my_transactions(user)
    txn_id = prompt_input("Transaction ID to pay")
    if not txn_id:
        return
    txn = find_transaction(txn_id)
    if not txn:
        print("  ✗ Transaction not found."); return
    if txn.status != "PENDING":
        print(f"  ✗ Transaction is {txn.status}, not PENDING."); return
    advance_transaction(txn_id, user)


def _show_my_transactions(user):
    txns = list_transactions_by_user(user.user_id)
    if not txns:
        print("\n  No transactions found."); return
    for txn in txns:
        show_transaction(txn, viewer_role=user.role)
        print("  ─────────────────────")