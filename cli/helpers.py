"""BridgeEscrow — CLI input helpers and display utilities."""


STATUS_DISPLAY = {"SHIPPED": "READY FOR DELIVERY"}


def prompt_input(label, hidden=False):
    """Prompt for user input, optionally hiding the text."""
    import getpass
    if hidden:
        return getpass.getpass(f"  {label}: ")
    return input(f"  {label}: ").strip()


def prompt_choice(label, options):
    """Display numbered options and return the chosen value."""
    print(f"\n  {label}:")
    for i, opt in enumerate(options, 1):
        print(f"    {i}. {opt}")
    choice = input("  Choice: ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(options): return options[idx]
    except ValueError:
        pass
    print("  ✗ Invalid choice."); return None


def confirm(message):
    """Ask a yes/no confirmation."""
    return input(f"  {message} (y/n): ").strip().lower() == "y"


def show_transaction(txn, viewer_role=None):
    """Pretty-print a single transaction."""
    status = STATUS_DISPLAY.get(txn.status, txn.status)
    print(f"\n  Transaction: {txn.txn_id}")
    print(f"  Product:   {txn.product_id}")
    print(f"  Buyer:     {txn.buyer_id}")
    print(f"  Retailer:  {txn.retailer_id}")
    print(f"  Amount:    KSh {txn.amount:,}")
    print(f"  Status:    {status}")
    if txn.delivery_id:
        print(f"  Delivery:  {txn.delivery_id}")
    if viewer_role == "BUYER" and txn.delivery_code and txn.status == "PAID":
        print(f"  Code:     {txn.delivery_code} — share with delivery person!")


def show_balance(user):
    """Display user balance info."""
    print(f"\n  Available: KSh {user.balance:,}")
    if user.locked:
        print(f"  Locked:    KSh {user.locked:,}")
        print(f"  Total:     KSh {user.balance + user.locked:,}")