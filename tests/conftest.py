import os, sys, json, tempfile, shutil
import pytest

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture
def tmp_data_dir(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for name in ["users", "products", "transactions", "payments", "ledger"]:
        (data_dir / f"{name}.json").write_text("[]")
    return data_dir


@pytest.fixture
def patched_db(tmp_data_dir, monkeypatch):
    import core.database as db

    new_files = {
        "users": str(tmp_data_dir / "users.json"),
        "products": str(tmp_data_dir / "products.json"),
        "transactions": str(tmp_data_dir / "transactions.json"),
        "payments": str(tmp_data_dir / "payments.json"),
        "ledger": str(tmp_data_dir / "ledger.json"),
    }
    monkeypatch.setattr(db, "FILES", new_files)
    monkeypatch.setattr(db, "DATA_DIR", str(tmp_data_dir))
    return db


@pytest.fixture
def sample_user(patched_db):
    from core.models import User

    user = User("B001", "Test Buyer", "testbuyer", "pass123", "BUYER", 200000)
    patched_db.save("users", [user.to_dict()])
    return user


@pytest.fixture
def sample_product(patched_db):
    from core.models import Product

    product = Product("P001", "Laptop", 85000, "R001", "A laptop", 10)
    patched_db.save("products", [product.to_dict()])
    return product


@pytest.fixture
def sample_retailer(patched_db):
    from core.models import User

    retailer = User("R001", "TestStore", "testretailer", "pass123", "RETAILER")
    patched_db.save("users", [retailer.to_dict()])
    return retailer


@pytest.fixture
def sample_delivery(patched_db):
    from core.models import User

    driver = User("D001", "TestDriver", "testdelivery", "pass123", "DELIVERY")
    patched_db.save("users", [driver.to_dict()])
    return driver


@pytest.fixture
def sample_trustee(patched_db):
    from core.models import User

    trustee = User("T001", "TestTrustee", "testtrustee", "pass123", "TRUSTEE")
    patched_db.save("users", [trustee.to_dict()])
    return trustee
