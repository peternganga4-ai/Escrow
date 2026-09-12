import core.config as config

import core.config as config
from .user_service import find_user_by_id, update_user
from .product_service import find_product, save_product
from .ledger import add_ledger_entry


def release_funds(txn):
    trustee_fee = int(txn.amount * config.TRUSTEE_FEE_PCT)
    delivery_fee = int(txn.amount * config.DELIVERY_FEE_PCT)
    retailer_payout = txn.amount - trustee_fee - delivery_fee
    retailer = find_user_by_id(txn.retailer_id)
    retailer.balance += retailer_payout
    update_user(retailer)
    driver = find_user_by_id(txn.delivery_id)
    driver.balance += delivery_fee
    update_user(driver)
    trustee = find_user_by_id("T001")
    trustee.balance += trustee_fee
    update_user(trustee)
    buyer = find_user_by_id(txn.buyer_id)
    buyer.locked -= txn.amount
    update_user(buyer)
    add_ledger_entry(txn.txn_id, "RELEASE", retailer_payout, to_id=retailer.user_id)
    add_ledger_entry(txn.txn_id, "DELIVERY_FEE", delivery_fee, to_id=driver.user_id)
    add_ledger_entry(txn.txn_id, "TRUSTEE_FEE", trustee_fee, to_id=trustee.user_id)


def refund_funds(txn):
    buyer = find_user_by_id(txn.buyer_id)
    buyer.balance += txn.amount
    buyer.locked -= txn.amount
    update_user(buyer)
    product = find_product(txn.product_id)
    product.stock += 1
    save_product(product)
    add_ledger_entry(txn.txn_id, "REFUND", txn.amount, to_id=buyer.user_id)
