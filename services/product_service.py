"""BridgeEscrow — Product catalogue operations."""

import core.database as db
import core.models as models


def list_products():
    """Return all products as Product objects."""
    return [models.Product.from_dict(p) for p in db.load("products")]


def find_product(product_id):
    """Find a product by ID. Returns Product or None."""
    for p in list_products():
        if p.product_id == product_id:
            return p
    return None


def save_product(product):
    """Persist an updated Product back to the data store."""
    products_data = db.load("products")
    for i, p in enumerate(products_data):
        if p["product_id"] == product.product_id:
            products_data[i] = product.to_dict()
            break
    db.save("products", products_data)


def display_products():
    """Pretty-print all available products."""
    products = list_products()
    if not products:
        print("\n  No products available.")
        return
    print("\n  ┌──────┬──────────────────┬──────────────┬────────────┬───────┐")
    print("  │ ID   │ Product          │ Retailer     │ Price(KSh) │ Stock│")
    print("  ├──────┼──────────────────┼──────────────┼────────────┼───────┤")
    for p in products:
        print(f"  │ {p.product_id:<4} │ {p.name:<16} "
              f"│ {p.retailer_id:<12} │ {p.price:>10,} │ {p.stock:>5} │")
    print("  └──────┴──────────────────┴──────────────┴────────────┴───────┘")
