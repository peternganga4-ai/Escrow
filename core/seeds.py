from .database import load, save
from .models import User, Product
from .config import BUYER_STARTING_BALANCE, RETAILER_STARTING_BALANCE
from .config import DELIVERY_STARTING_BALANCE


def seed_all():
    if load("users"):
        return
    demo_users = [
        User(
            "B001", "John Buyer", "buyer", "buyer123", "BUYER", BUYER_STARTING_BALANCE
        ),
        User("B002", "Alice Buyer", "alice", "buyer123", "BUYER", 150000),
        User(
            "R001",
            "TechStore",
            "retailer",
            "retailer123",
            "RETAILER",
            RETAILER_STARTING_BALANCE,
        ),
        User(
            "R002",
            "GadgetHub",
            "retailer2",
            "retailer123",
            "RETAILER",
            RETAILER_STARTING_BALANCE,
        ),
        User(
            "D001",
            "FastDeliver",
            "delivery",
            "delivery123",
            "DELIVERY",
            DELIVERY_STARTING_BALANCE,
        ),
        User(
            "D002",
            "QuickShip",
            "shipper",
            "delivery123",
            "DELIVERY",
            DELIVERY_STARTING_BALANCE,
        ),
        User("T001", "TrustBoard", "trustee", "trustee123", "TRUSTEE", 0),
    ]
    save("users", [u.to_dict() for u in demo_users])

    demo_products = [
        Product("P001", "Laptop", 85000, "R001", "High-performance laptop", 10),
        Product("P002", "iPhone", 80000, "R001", "Latest iPhone model", 15),
        Product("P003", "Headphones", 5000, "R002", "Wireless noise-cancelling", 30),
        Product("P004", "Keyboard", 3500, "R002", "Mechanical gaming keyboard", 20),
        Product("P005", "Monitor", 45000, "R001", "27-inch 4K monitor", 8),
    ]
    save("products", [p.to_dict() for p in demo_products])
