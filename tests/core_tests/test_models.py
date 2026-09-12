from core.models import User, Product


class TestUser:
    def test_user_to_dict_roundtrip(self):
        u = User("B001", "John", "john", "pass", "BUYER", 200000)
        u.locked = 50000
        d = u.to_dict()
        restored = User.from_dict(d)
        assert restored.user_id == "B001"
        assert restored.name == "John"
        assert restored.username == "john"
        assert restored.role == "BUYER"
        assert restored.balance == 200000
        assert restored.locked == 50000

    def test_user_default_balance(self):
        u = User("R001", "Store", "store", "p", "RETAILER")
        assert u.balance == 0
        assert u.locked == 0

    def test_user_from_dict_missing_balance(self):
        d = {
            "user_id": "B001",
            "name": "A",
            "username": "a",
            "password": "p",
            "role": "BUYER",
        }
        u = User.from_dict(d)
        assert u.balance == 0
        assert u.locked == 0


class TestProduct:
    def test_product_to_dict_roundtrip(self):
        p = Product("P001", "Laptop", 85000, "R001", "Nice", 10)
        d = p.to_dict()
        restored = Product.from_dict(d)
        assert restored.product_id == "P001"
        assert restored.name == "Laptop"
        assert restored.price == 85000
        assert restored.stock == 10

    def test_product_defaults(self):
        p = Product("P002", "Mouse", 1000, "R001")
        assert p.description == ""
        assert p.stock == 0

    def test_product_from_dict_missing_optional(self):
        d = {"product_id": "P001", "name": "X", "price": 100, "retailer_id": "R001"}
        p = Product.from_dict(d)
        assert p.description == ""
        assert p.stock == 0
