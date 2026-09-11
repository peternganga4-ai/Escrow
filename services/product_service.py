"""product catalogue operations"""

import core.database as db
import core.models as models


def list_products():
    #products returned as objects
    return [models.Product.from_dict
    (p) for p in db.load("products")]


