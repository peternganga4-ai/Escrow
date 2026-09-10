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


def test_login_unknown_user(patched_db, capsys):
    auth = AuthManager()
    result = auth.login("nobody", "pass123")
    assert result is None


def test_logout_clears_session(patched_db, sample_user, capsys):
    auth = AuthManager()
    auth.login("testbuyer", "pass123")
    auth.logout()
    assert not auth.is_authenticated()
    assert auth.current_user is None


def test_has_role(patched_db, sample_user, capsys):
    auth = AuthManager()
    auth.login("testbuyer", "pass123")
    assert auth.has_role("BUYER")
    assert not auth.has_role("RETAILER")


def test_require_role_success(patched_db, sample_user, capsys):
    auth = AuthManager()
    auth.login("testbuyer", "pass123")
    assert auth.require_role("BUYER")


def test_require_role_failure(patched_db, sample_user, capsys):
    auth = AuthManager()
    auth.login("testbuyer", "pass123")
    assert not auth.require_role("TRUSTEE")


def test_require_role_not_logged_in(capsys):
    auth = AuthManager()
    assert not auth.require_role("BUYER")