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
#logout method $ display message with the current user name
    def logout(self):
         if self.current_user:
              print(f"\n Goodbye, {self.current_user.name}!")
              self.current_user = None
#Actual check for login user
    def is_authenticated(self):
         return self.current_user is not None

#creates method $ gives the roles to auth personel
    def has_role(self, *roles):
         return self.is_authenticated() and self.current_user.role in roles
#defines roles&gives several roles
    def require_role(self, *roles):

         #checks whether login is auth&display themessage
         if not self.is_authenticated():
              print("\n You must be logged in.")
              return False

         #calls has_role method and unpacks tuple
         if not self.has_role(*roles):
              #displays message&joins the roles whether retailer or buyer
              print(f"\n Access denied.Required: {','.join(roles)}")
              return False
         return True
    
    
              

    

