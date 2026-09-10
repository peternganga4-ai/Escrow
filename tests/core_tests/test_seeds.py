


def test_seed_all_creates_users(patched_db):
    from core.seeds import seed_all
    seed_all()
    users = patched_db.load("users")
    assert len(users) > 0
    assert users[0]["user_id"].startswith("B")


def test_seed_all_creates_products(patched_db):
    from core.seeds import seed_all
    seed_all()
    products = patched_db.load("products")
    assert len(products) > 0
    assert products[0]["product_id"].startswith("P")


def test_seed_all_idempotent(patched_db):
    from core.seeds import seed_all
    seed_all()
    users_after_first = patched_db.load("users")
    seed_all()
    users_after_second = patched_db.load("users")
    assert len(users_after_first) == len(users_after_second)


def test_seeded_buyer_has_200k(patched_db):
    from core.seeds import seed_all
    seed_all()
    users = patched_db.load("users")
    buyers = [u for u in users if u["role"] == "BUYER"]
    assert buyers[0]["balance"] == 200000


def test_seeded_retailer_has_100k(patched_db):
    from core.seeds import seed_all
    seed_all()
    users = patched_db.load("users")
    retailers = [u for u in users if u["role"] == "RETAILER"]
    assert retailers[0]["balance"] == 100000


def test_seeded_delivery_has_50k(patched_db):
    from core.seeds import seed_all
    seed_all()
    users = patched_db.load("users")
    drivers = [u for u in users if u["role"] == "DELIVERY"]
    assert drivers[0]["balance"] == 50000


def test_seeded_trustee_has_zero(patched_db):
    from core.seeds import seed_all
    seed_all()
    users = patched_db.load("users")
    trustees = [u for u in users if u["role"] == "TRUSTEE"]
    assert trustees[0]["balance"] == 0