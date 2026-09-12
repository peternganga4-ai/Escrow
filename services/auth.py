from .user_service import find_user_by_username


class AuthManager:

    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        user = find_user_by_username(username)
        if not user or user.password != password:
            print("\nInvalid username or password.")
            return None
        self.current_user = user
        print(f"\nWelcome, {user.name}! Role: {user.role}")
        return user

    def logout(self):
        if self.current_user:
            print(f"\nGoodbye, {self.current_user.name}!")
            self.current_user = None

    def is_authenticated(self):
        return self.current_user is not None

    def has_role(self, *roles):
        return self.is_authenticated() and self.current_user.role in roles

    def require_role(self, *roles):
        if not self.is_authenticated():
            print("\nYou must be logged in.")
            return False
        if not self.has_role(*roles):
            print(f"\nAccess denied. Required: {', '.join(roles)}")
            return False
        return True
