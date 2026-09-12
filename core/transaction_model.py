from .config import TXN_STATUS_FLOW


class Transaction:

    def __init__(
        self,
        txn_id,
        product_id,
        buyer_id,
        retailer_id,
        amount,
        status="PENDING",
        delivery_code=None,
    ):
        self.txn_id = txn_id
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.retailer_id = retailer_id
        self.amount = amount
        self.status = status
        self.delivery_id = None
        self.delivery_code = delivery_code

    def next_status(self):
        if self.status not in TXN_STATUS_FLOW:
            return None
        idx = TXN_STATUS_FLOW.index(self.status)
        if idx + 1 < len(TXN_STATUS_FLOW):
            return TXN_STATUS_FLOW[idx + 1]
        return None

    def to_dict(self):
        return {
            "txn_id": self.txn_id,
            "product_id": self.product_id,
            "buyer_id": self.buyer_id,
            "retailer_id": self.retailer_id,
            "amount": self.amount,
            "status": self.status,
            "delivery_id": self.delivery_id,
            "delivery_code": self.delivery_code,
        }

    @classmethod
    def from_dict(cls, d):
        t = cls(
            d["txn_id"],
            d["product_id"],
            d["buyer_id"],
            d["retailer_id"],
            d["amount"],
            d.get("status", "PENDING"),
            d.get("delivery_code"),
        )
        t.delivery_id = d.get("delivery_id")
        return t
