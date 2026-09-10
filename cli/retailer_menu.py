"""BridgeEscrow — Retailer CLI menu."""

from .helpers import prompt_input, show_transaction, show_balance
from services.transaction_service import list_transactions_by_user, advance_transaction


def retailer_menu(auth):
    """Interactive menu for RETAILER users."""
    user = auth.current_user
    while True:
        print(f"\n── Retailer Menu ({user.name}) ──")
        print("  1. My Transactions")
        print("  2. Mark Ready for Delivery")
        print("  3. My Balance")
        print("  4. Logout")
        choice = input("  Choice: ").strip()
        if choice == "1": _show_my_transactions(user)
        elif choice == "2": _delivery_flow(user)
        elif choice == "3": show_balance(user)
        elif choice == "4": auth.logout(); break
        else: print("  ✗ Invalid choice.")


def _show_my_transactions(user):
    txns = list_transactions_by_user(user.user_id)
    if not txns: print("\n  No transactions found."); return
    for txn in txns:
        show_transaction(txn); print("  ─────────────────────")


def _delivery_flow(user):
    txn_id = prompt_input("Transaction ID to mark ready")
    if not txn_id: return
    txn = advance_transaction(txn_id, user)
    if txn: show_transaction(txn)