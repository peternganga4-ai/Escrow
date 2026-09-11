"""BridgeEscrow — Global configuration and constants."""

DATA_DIR_NAME = "data"

ROLE_PREFIX = {
    "BUYER": "B",
    "RETAILER": "R",
    "DELIVERY": "D",
    "TRUSTEE": "T",
}

VALID_ROLES = set(ROLE_PREFIX)

# Roles users can self-register as (TRUSTEE is invite-only)
REGISTRABLE_ROLES = ["BUYER", "RETAILER", "DELIVERY"]

TXN_STATUS_FLOW = [
    "PENDING", "PAID", "SHIPPED",
    "DELIVERED", "REFUNDED",
]

ROLE_PERMISSIONS = {
    "BUYER": ["PAID"],
    "RETAILER": ["SHIPPED"],
    "DELIVERY": ["DELIVERED"],
    "TRUSTEE": ["REFUNDED"],
}

BUYER_STARTING_BALANCE = 200000
RETAILER_STARTING_BALANCE = 100000
DELIVERY_STARTING_BALANCE = 50000
TRUSTEE_STARTING_BALANCE = 0

# Fee percentages
DELIVERY_FEE_PCT = 0.03   # 3% delivery fee
TRUSTEE_FEE_PCT = 0.01   # 1% trustee commission

# Starting balances by role (used by user_service)
BALANCE_BY_ROLE = {
    "BUYER": BUYER_STARTING_BALANCE,
    "RETAILER": RETAILER_STARTING_BALANCE,
    "DELIVERY": DELIVERY_STARTING_BALANCE,
    "TRUSTEE": TRUSTEE_STARTING_BALANCE,
}

# No refund allowed once funds are released
NO_REFUND_STATUSES = {"RELEASED"}
