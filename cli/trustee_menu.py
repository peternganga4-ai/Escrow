"""BridgeEscrow — Trustee CLI menu."""

from .helpers import prompt_input, show_transaction, show_balance
from services.transaction_service import advance_transaction
from core.database import load
from core.transaction_model import Transaction


def trustee_menu(auth):
    """Interactive menu for TRUSTEE users."""
    user = auth.current_user
    while True:
        print(f"\n── Trustee Menu ({user.name}) ──")
        print("  1. All Transactions")
        print("  2. Refund Transaction")
        print("  3. My Balance")
        print("  4. Logout")
        choice = input("  Choice: ").strip()
        if choice == "1": _show_all_transactions()
        elif choice == "2": _refund_flow(user)
        elif choice == "3": show_balance(user)
        elif choice == "4": auth.logout(); break
        else: print("  ✗ Invalid choice.")


def _show_all_transactions():
    all_txns = [Transaction.from_dict(t) for t in load("transactions")]
    if not all_txns: print("\n  No transactions found."); return
    for txn in all_txns:
        show_transaction(txn); print("  ─────────────────────")


def _refund_flow(user):
    txn_id = prompt_input("Transaction ID to refund")
    if not txn_id: return
    txn = advance_transaction(txn_id, user)
    if txn: show_transaction(txn)