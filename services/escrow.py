"""BridgeEscrow fund release and refund logic"""

#import modules and reliable functions
import core.config as config
from .user_service import find_user_by_id, update_user
from .product_service import find_product, save_product
from .ledger import add_ledger_entry


def release_funds(txn):
    #release held escrow:R gets goods value minus fees,delivery agent gets delivery fee,trustee gets commission.
    trustee_fee = int(txn.amount * config.TRUSTEE_FEE_PCT)
    delivery_fee = int(txn.amount * config.DELIVERY_FEE_PCT)
    retailer_payout = txn.amount - trustee_fee - delivery_fee

    #pay retailer
    retailer = find_user_by_id(txn.retailer_id)
    retailer.balance += retailer_payout
    update_user(retailer)
    #pay trustee
    trustee = find_user_by_id("T001")
    trustee.balance += trustee_fee
    update_user(trustee)
