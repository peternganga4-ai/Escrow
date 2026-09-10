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

