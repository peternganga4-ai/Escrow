"""Tests for services.auth — AuthManager login/logout/roles."""

from services.auth import AuthManager
from services.user_service import register_user

def test_login_success(patched_db, sample_user, capsys):
    auth = AuthManager()
    result = auth.login("testbuyer", "pass123")
    assert result is not None
    assert auth.is_authenticated()
    assert auth.current_user.user_id == "B001"



def test_login_wrong_password(patched_db, sample_user, capsys):
    auth = AuthManager()
    result = auth.login("testbuyer", "wrongpass")
    assert result is None
    assert not auth.is_authenticated()
