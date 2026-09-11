"""BridgeEscrow — Authentication and session management."""

from .user_service import find_user_by_username


class AuthManager:
    """Manages user authentication and session state."""

    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        user = find_user_by_username(username)
        if not user or user.password != password:
            print("\n✗ Invalid username or password.")
            return None
        self.current_user = user
        print(f"\n✓ Welcome, {user.name}! Role: {user.role}")
        return user

    def logout(self):
        if self.current_user:
            print(f"\n✓ Goodbye, {self.current_user.name}!")
            self.current_user = None

    def is_authenticated(self):
        return self.current_user is not None

    def has_role(self, *roles):
        return self.is_authenticated() and self.current_user.role in roles

    def require_role(self, *roles):
        if not self.is_authenticated():
            print("\n✗ You must be logged in.")
            return False
        if not self.has_role(*roles):
            print(f"\n✗ Access denied. Required: {', '.join(roles)}")
            return False
        return True
