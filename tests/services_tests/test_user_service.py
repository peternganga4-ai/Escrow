"""Tests for services.user_service."""

import pytest
from core.models import User
from services.user_service import register_user, find_user_by_id


def test_register_buyer_gets_200k(patched_db):
    user = register_user("Alice", "alice", "p", "BUYER")
    assert user.balance == 200000


def test_register_retailer_gets_100k(patched_db):
    user = register_user("Store", "store", "p", "RETAILER")
    assert user.balance == 100000


def test_register_delivery_gets_50k(patched_db):
    user = register_user("Driver", "driver", "p", "DELIVERY")
    assert user.balance == 50000



def test_register_trustee_not_allowed(patched_db):
    with pytest.raises(ValueError, match="not available"):
        register_user("Trust", "trust", "p", "TRUSTEE")


def test_register_duplicate_username_raises(patched_db):
    register_user("Bob", "bob", "p", "BUYER")
    with pytest.raises(ValueError, match="already exists"):
        register_user("Bob2", "bob", "p", "BUYER")



def test_register_invalid_role_raises(patched_db):
    with pytest.raises(ValueError, match="not available"):
        register_user("Hack", "hacker", "p", "HACKER")


def test_find_user_by_username(patched_db):
    register_user("Carol", "carol", "p", "BUYER")
    from services.user_service import find_user_by_username
    assert find_user_by_username("carol").username == "carol"




def test_find_user_by_username_not_found(patched_db):
    from services.user_service import find_user_by_username
    assert find_user_by_username("nobody") is None


def test_find_user_by_id(patched_db):
    user = register_user("Dave", "dave", "p", "RETAILER")
    assert find_user_by_id(user.user_id).username == "dave"


def test_update_user_persists(patched_db):
    user = register_user("Eve", "eve", "p", "BUYER")
    user.balance = 500
    from services.user_service import update_user
    update_user(user)
    assert find_user_by_id(user.user_id).balance == 500