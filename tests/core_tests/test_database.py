"""Tests for core.database — load/save operations."""

import json


def test_load_empty_key_returns_list(patched_db):
    """Loading an empty key should return an empty list."""
    result = patched_db.load("users")
    assert result == []


def test_save_and_load_roundtrip(patched_db):
    """Data saved should be retrievable unchanged."""
    data = [{"id": "U001", "name": "Alice"}]
    patched_db.save("users", data)
    result = patched_db.load("users")
    assert result == data


def test_save_creates_file(patched_db, tmp_data_dir):
    """Saving should create the JSON file on disk."""
    patched_db.save("users", [{"id": "1"}])
    assert (tmp_data_dir / "users.json").exists()


def test_save_overwrites_existing(patched_db):
    """Saving should overwrite previously saved data."""
    patched_db.save("users", [{"id": "1"}])
    patched_db.save("users", [{"id": "2"}])
    result = patched_db.load("users")
    assert result == [{"id": "2"}]


def test_load_all_keys(patched_db):
    """All defined keys should be loadable."""
    for key in patched_db.FILES:
        result = patched_db.load(key)
        assert isinstance(result, list)


def test_saved_json_is_pretty_formatted(patched_db, tmp_data_dir):
    """Saved files should use indent=2 formatting."""
    patched_db.save("users", [{"id": "1"}])
    content = (tmp_data_dir / "users.json").read_text()
    assert '\n' in content  # Pretty-printed has newlines
    parsed = json.loads(content)
    assert parsed == [{"id": "1"}]
