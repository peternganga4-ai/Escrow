def test_main_menu_exit(monkeypatch, capsys):
    from cli.main import main

    monkeypatch.setattr("builtins.input", lambda _: "3")
    main()
    assert "Goodbye" in capsys.readouterr().out


def test_register_flow(monkeypatch, patched_db, capsys):
    from cli.main import _register_flow

    inputs = iter(["Alice", "alice", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("getpass.getpass", lambda _: "pass123")
    _register_flow()
    assert "Registered" in capsys.readouterr().out


def test_login_flow_fail(monkeypatch, patched_db, capsys):
    from cli.main import _login_flow
    from services.auth import AuthManager

    auth = AuthManager()
    monkeypatch.setattr("builtins.input", lambda _: "nobody")
    monkeypatch.setattr("getpass.getpass", lambda _: "wrong")
    _login_flow(auth)
    assert "Invalid" in capsys.readouterr().out


def test_main_welcome_banner(capsys, monkeypatch):
    from cli.main import main

    monkeypatch.setattr("builtins.input", lambda _: "3")
    main()
    assert "BridgeEscrow" in capsys.readouterr().out


def test_main_invalid_choice(monkeypatch, capsys):
    from cli.main import main

    inputs = iter(["9", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    main()
    assert "Invalid" in capsys.readouterr().out


def test_register_no_trustee_option(patched_db, capsys):
    import core.config as config

    assert "TRUSTEE" not in config.REGISTRABLE_ROLES
