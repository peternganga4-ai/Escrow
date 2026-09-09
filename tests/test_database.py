import json

def test_load_empty_key_returns_list(patched_db):
    result = patched_db.load("users")
    assert result == []


def test_save_and_load_roundtrip(patched_db):
    data = [{"id": "U001", "name": "Alice"}]
    patched_db.save("users", data)
    result = patched_db.load("users")
    assert result == data


def test_save_creates_file(patched_db, tmp_data_dir):
    patched_db.save("users", [{"id": "1"}])
    assert (tmp_data_dir / "users.json").exists()


def test_save_overwrites_existing(patched_db):
    patched_db.save("users", [{"id": "1"}])
    patched_db.save("users", [{"id": "2"}])
    result = patched_db.load("users")
    assert result == [{"id": "2"}]


def test_load_all_keys(patched_db):
    for key in patched_db.FILES:
        result = patched_db.load(key)
        assert isinstance(result, list)


def test_saved_json_is_pretty_formatted(patched_db, tmp_data_dir):
    patched_db.save("users", [{"id": "1"}])
    content = (tmp_data_dir / "users.json").read_text()
    assert "\n" in content
    parsed = json.loads(content)
    assert parsed == [{"id": "1"}]
