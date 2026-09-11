"""product catalogue operations"""

import core.database as db
import core.models as models


def list_products():
    #products returned as objects
    return [models.Product.from_dict
    (p) for p in db.load("products")]

# updating product back to the data base
def save_product(product):
    
    products_data = db.load("products")
    for i, p in enumerate(products_data):
        if p["product_id"] == product.product_id:
            products_data[i] = product.to_dict()
            break
    db.save("products", products_data)


#print all products available by displaying on terminal
def display_products():
    
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


