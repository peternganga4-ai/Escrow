"""Tests for services.user_service."""

import pytest
from core.models import User
from services.user_service import register_user, find_user_by_id


def test_register_buyer_gets_200k(patched_db):
    user = register_user("Alice", "alice", "p", "BUYER")
    assert user.balance == 200000


