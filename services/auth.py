"""BridgeEscrow - Authentication and session management.."""

from .user_service import find_user_by_username


#User authentication
class AuthManager:
    def __init__(self):
        self.current_user = None
#login method created
    def login(self, username, password):
        user = find_user_by_username (username)
        #checks login whether should be rejected
        if not user or user.password !=password:
              print("\n Invalid username or password.")
              return None
#saves the user login and display a message
        self.current_user = user
        print(f"\n Welcome, {user.name}! Role: {user.role}")
        return user

    def logout(self):
         if

    

