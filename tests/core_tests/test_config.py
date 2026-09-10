

import core.config as config


def test_valid_roles_match_prefix_keys():
    assert config.VALID_ROLES == set(config.ROLE_PREFIX)


def test_role_prefix_values():
    assert config.ROLE_PREFIX["BUYER"] == "B"
    assert config.ROLE_PREFIX["RETAILER"] == "R"
    assert config.ROLE_PREFIX["DELIVERY"] == "D"
    assert config.ROLE_PREFIX["TRUSTEE"] == "T"


def test_registrable_roles_exclude_trustee():
    assert "TRUSTEE" not in config.REGISTRABLE_ROLES
    assert set(config.REGISTRABLE_ROLES) < config.VALID_ROLES


def test_status_flow_order():
    flow = config.TXN_STATUS_FLOW
    assert flow[0] == "PENDING"
    assert flow[1] == "PAID"
    assert "DELIVERED" in flow
    assert "REFUNDED" in flow


def test_role_permissions_keys_match_roles():
    for role in config.ROLE_PERMISSIONS:
        assert role in config.VALID_ROLES


def test_buyer_can_pay():
    assert "PAID" in config.ROLE_PERMISSIONS["BUYER"]


def test_trustee_can_refund():
    assert "REFUNDED" in config.ROLE_PERMISSIONS["TRUSTEE"]


def test_buyer_starting_balance_positive():
    assert config.BUYER_STARTING_BALANCE > 0


def test_delivery_fee_pct():
    assert config.DELIVERY_FEE_PCT == 0.03


def test_trustee_fee_pct():
    assert config.TRUSTEE_FEE_PCT == 0.01


def test_no_refund_statuses_contains_released():
    assert "RELEASED" in config.NO_REFUND_STATUSES


def test_balance_by_role_covers_all_roles():
    for role in config.VALID_ROLES:
        assert role in config.BALANCE_BY_ROLE