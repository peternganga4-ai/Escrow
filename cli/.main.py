"""BridgeEscrow — Main entry point and login menu."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

import core.config as config
from core import seed_all
from services.auth import AuthManager
from services.user_service import register_user
from .helpers import prompt_input, prompt_choice
from .buyer_menu import buyer_menu
from .retailer_menu import retailer_menu
from .delivery_menu import delivery_menu
from .trustee_menu import trustee_menu

ROLE_MENUS = {"BUYER": buyer_menu, "RETAILER": retailer_menu,
              "DELIVERY": delivery_menu, "TRUSTEE": trustee_menu}


def main():
    """Run the BridgeEscrow application."""
    seed_all(); auth = AuthManager()
    while True:
        print("\n╔══════════════════════════╗")
        print("║    BridgeEscrow System    ║")
        print("╠══════════════════════════╣")
        print("║  1. Login                ║")
        print("║  2. Register             ║")
        print("║  3. Exit                 ║")
        print("╚══════════════════════════╝")
        choice = input("  Choice: ").strip()
        if choice == "1": _login_flow(auth)
        elif choice == "2": _register_flow()
        elif choice == "3": print("\n  Goodbye!"); break
        else: print("  ✗ Invalid choice.")


def _login_flow(auth):
    username = prompt_input("Username")
    password = prompt_input("Password", hidden=True)
    user = auth.login(username, password)
    if user:
        menu_fn = ROLE_MENUS.get(user.role)
        if menu_fn: menu_fn(auth)


def _register_flow():
    name = prompt_input("Full name")
    username = prompt_input("Username")
    password = prompt_input("Password", hidden=True)
    role = prompt_choice("Select role", config.REGISTRABLE_ROLES)
    if not role: return
    try:
        user = register_user(name, username, password, role)
        print(f"\n✓ Registered as {user.user_id} ({user.role})")
    except ValueError as e:
        print(f"\n✗ {e}")

if __name__ == "__main__":
    main()