"""BridgeEscrow — Delivery CLI menu."""

from .helpers import prompt_input, show_transaction, show_balance
from services.transaction_service import advance_transaction
from core.database import load
from core.transaction_model import Transaction


def delivery_menu(auth):
    """Interactive menu for DELIVERY users."""
    user = auth.current_user
    while True:
        print(f"\n── Delivery Menu ({user.name}) ──")
        print("  1. Available Deliveries")
        print("  2. Confirm Delivery")
        print("  3. My Balance")
        print("  4. Logout")
        choice = input("  Choice: ").strip()
        if choice == "1": _show_available_deliveries()
        elif choice == "2": _deliver_flow(user)
        elif choice == "3": show_balance(user)
        elif choice == "4": auth.logout(); break
        else: print("  ✗ Invalid choice.")


def _show_available_deliveries():
    all_txns = [Transaction.from_dict(t) for t in load("transactions")]
    available = [t for t in all_txns if t.status == "SHIPPED"]
    if not available: print("\n  No deliveries waiting."); return
    print("\n  Deliveries ready for pickup:")
    for txn in available:
        show_transaction(txn); print("  ─────────────────────")


def _deliver_flow(user):
    txn_id = prompt_input("Transaction ID to deliver")
    if not txn_id: return
    code = prompt_input("Delivery code (from buyer)")
    if not code: print("  ✗ Delivery code required."); return
    txn = advance_transaction(txn_id, user, code=code)
    if txn: show_transaction(txn)