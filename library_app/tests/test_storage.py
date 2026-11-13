import json

from library_app.library import Library
from library_app.models import EBook
from library_app.storage import load, save


def test_round_trip_preserves_everything(lib, tmp_path):
    lib.checkout(1, "111")
    lib.checkout(1, "444")
    path = tmp_path / "lib.json"

    save(lib, path)
    loaded = load(path)

    assert loaded.name == lib.name
    assert list(loaded) == list(lib)
    assert isinstance(loaded["444"], EBook)           # type survives
    assert loaded["444"].file_size_mb == 2.4
    alice = next(m for m in loaded.members() if m.member_id == 1)
    assert [b.isbn for b in alice.borrowed] == ["111", "444"]
    assert [b.isbn for b in loaded.available_books()] == ["222", "333"]
    assert alice.joined == next(m for m in lib.members() if m.member_id == 1).joined


def test_load_missing_file_gives_empty_library(tmp_path):
    loaded = load(tmp_path / "nope.json")
    assert isinstance(loaded, Library)
    assert len(loaded) == 0


def test_saved_file_is_valid_json_with_only_isbns_for_loans(lib, tmp_path):
    lib.checkout(2, "222")
    path = tmp_path / "lib.json"
    save(lib, path)
    data = json.loads(path.read_text())
    bob = next(m for m in data["members"] if m["member_id"] == 2)
    assert bob["borrowed"] == ["222"]
