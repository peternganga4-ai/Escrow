"""BridgeEscrow — Data models: User, Product."""

from .config import BUYER_STARTING_BALANCE, RETAILER_STARTING_BALANCE
from .config import DELIVERY_STARTING_BALANCE, TRUSTEE_STARTING_BALANCE


BALANCE_BY_ROLE = {
    "BUYER": BUYER_STARTING_BALANCE,
    "RETAILER": RETAILER_STARTING_BALANCE,
    "DELIVERY": DELIVERY_STARTING_BALANCE,
    "TRUSTEE": TRUSTEE_STARTING_BALANCE,
}


class User:
    """Represents a system user with role-based access."""

    def __init__(self, user_id, name, username, password, role, balance=0):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self.balance = balance
        self.locked = 0

    def to_dict(self):
        return {
            "user_id": self.user_id, "name": self.name,
            "username": self.username, "password": self.password,
            "role": self.role, "balance": self.balance,
            "locked": self.locked,
        }

    @classmethod
    def from_dict(cls, d):
        u = cls(d["user_id"], d["name"], d["username"],
               d["password"], d["role"], d.get("balance", 0))
        u.locked = d.get("locked", 0)
        return u


class Product:
    """Represents a product listing."""

    def __init__(self, product_id, name, price, retailer_id,
                 description="", stock=0):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.retailer_id = retailer_id
        self.description = description
        self.stock = stock

    def to_dict(self):
        return {
            "product_id": self.product_id, "name": self.name,
            "price": self.price, "retailer_id": self.retailer_id,
            "description": self.description, "stock": self.stock,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["product_id"], d["name"], d["price"],
                  d["retailer_id"], d.get("description", ""),
                  d.get("stock", 0))