import core.database as db
import core.models as models


def list_products():
    return [models.Product.from_dict(p) for p in db.load("products")]


def find_product(product_id):
    for p in list_products():
        if p.product_id == product_id:
            return p
    return None


def save_product(product):
    products_data = db.load("products")
    for i, p in enumerate(products_data):
        if p["product_id"] == product.product_id:
            products_data[i] = product.to_dict()
            break
    db.save("products", products_data)


def display_products():
    products = list_products()
    if not products:
        print("\n  No products available.")
        return
    print("\n  ID | Product | Retailer | Price(KSh) | Stock")
    for p in products:
        print(
            f"  {p.product_id} | {p.name} | {p.retailer_id} "
            f"| {p.price:,} | {p.stock}"
        )
