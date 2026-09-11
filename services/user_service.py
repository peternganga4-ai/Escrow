"""BridgeEscrow - user CRUD operations"""


import core.database as db
import core.models as models
import core.config as config
from .ledger import add_ledger_entry

#generating user Id basedon role prefix
def _next_user_id(role):
    #gets roleby prefix
    prefix = config.ROLE_PREFIX.get(role, "U")
    #load users data from db
    users = db.load("users")
    nums = []


    #generator expression
    for uid in (u["user_id"] for u in users):
        if uid.startswith(prefix) and uid[1:].isdigit():
            nums.append(int(uid[1:]))
            return f"{prefix}{max(nums) + 1 if nums else 1:03d}"


def register_user(name, username, password, role):
    #register new user and returns user or valueError
    users_data = db.load("users")
    if any(u["username"] == username for u in users_data):
        raise ValueError(f"Username '{username}' already exists.")
    role = role.upper()
    if role not in config.REGISTRABLE_ROLES:
        raise ValueError(
            f"Role '{role}' is not available for registration.")
    user_id = _next_user_id(role)
    balance = config.BALANCE_BY_ROLE.get(role, 0)
    user = models.User(user_id, name, username, password, role,
                      balance=balance)
    users_data.append(user.to_dict())
    db.save("users", users_data)
    if balance > 0:
        add_ledger_entry("--", "SEED", balance, to_id=user_id)
    return user   



#  finding username in db
def find_user_by_username(username):
    for u in db.load("users"):
        if u["username"] == username:
            return models.User.from_dict(u)
    return None

#find by id
def find_user_by_id(user_id):
    for u in db.load("users"):
        if u["user_id"] == user_id:
            return models.User.from_dict(u)
    return None


#update CRUD part taking existig user object
def update_user(user):
    users_data = db.load("users")
    for i, u in enumerate(users_data):
        if u["user_id"] == user.user_id:
            users_data[i] = user.to_dict()
            break
    db.save("users", users_data)