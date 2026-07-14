"""이전에 확인된 동작이 이후 변경으로 깨지지 않는지 확인하는 회귀 테스트.

여기 테스트들은 실제로 문제가 되었거나 될 수 있는 경계 케이스를 다룬다.
새 기능을 추가하거나 리팩터링할 때 이 파일이 계속 통과해야 한다.
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from json_lib import load_json, parse_json, save_json
from json_crud import create_item, read_all, read_by_id, update_item, delete_item


def test_load_missing_file_raises():
    """존재하지 않는 파일을 load_json으로 읽으면 조용히 None이 아니라 예외가 나야 한다."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        missing_path = Path(tmp_dir) / "nope.json"
        try:
            load_json(missing_path)
            assert False, "FileNotFoundError가 발생해야 한다"
        except FileNotFoundError:
            pass

    print("test_load_missing_file_raises: PASS")


def test_parse_invalid_json_raises():
    """깨진 JSON 문자열은 명확한 예외를 발생시켜야 한다."""
    try:
        parse_json("{invalid json")
        assert False, "json.JSONDecodeError가 발생해야 한다"
    except json.JSONDecodeError:
        pass

    print("test_parse_invalid_json_raises: PASS")


def test_save_preserves_types_and_unicode():
    """int/float/bool/None/list/dict/한글 문자열이 저장 후에도 그대로 유지돼야 한다."""
    data = {
        "int": 42,
        "float": 3.14,
        "bool": False,
        "none": None,
        "list": [1, "두", 3.0],
        "unicode": "한글 테스트 🎉",
        "empty_dict": {},
        "empty_list": [],
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "types.json"
        save_json(data, file_path)
        loaded = load_json(file_path)
        assert loaded == data

        # 한글이 \uXXXX로 이스케이프되지 않고 그대로 저장돼야 한다 (ensure_ascii=False).
        raw_text = file_path.read_text(encoding="utf-8")
        assert "한글 테스트" in raw_text

    print("test_save_preserves_types_and_unicode: PASS")


def test_crud_missing_file_starts_empty():
    """CRUD 대상 파일이 없을 때 read_all은 빈 목록을, create_item은 새 파일을 만든다."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "records.json"

        assert read_all(file_path) == []
        assert not file_path.exists()

        create_item(file_path, {"id": 1, "name": "first"})
        assert file_path.exists()
        assert read_all(file_path) == [{"id": 1, "name": "first"}]

    print("test_crud_missing_file_starts_empty: PASS")


def test_crud_id_reuse_after_delete():
    """삭제된 id는 이후 같은 값으로 다시 create할 수 있어야 한다."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "records.json"

        create_item(file_path, {"id": 1, "name": "old"})
        delete_item(file_path, 1)
        create_item(file_path, {"id": 1, "name": "new"})

        record = read_by_id(file_path, 1)
        assert record == {"id": 1, "name": "new"}

    print("test_crud_id_reuse_after_delete: PASS")


def test_crud_update_does_not_add_unrelated_fields():
    """update_item은 지정한 필드 외 다른 레코드에는 영향을 주지 않는다."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "records.json"

        create_item(file_path, {"id": 1, "name": "사과", "price": 1000})
        create_item(file_path, {"id": 2, "name": "바나나", "price": 500})

        update_item(file_path, 1, {"price": 1500})

        untouched = read_by_id(file_path, 2)
        assert untouched == {"id": 2, "name": "바나나", "price": 500}

    print("test_crud_update_does_not_add_unrelated_fields: PASS")


def test_crud_custom_id_field():
    """id_field를 다른 이름으로 지정해도 create/read/update/delete가 모두 동작해야 한다."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "users.json"

        create_item(file_path, {"user_no": 100, "name": "홍길동"}, id_field="user_no")
        found = read_by_id(file_path, 100, id_field="user_no")
        assert found == {"user_no": 100, "name": "홍길동"}

        update_item(file_path, 100, {"name": "홍길순"}, id_field="user_no")
        updated = read_by_id(file_path, 100, id_field="user_no")
        assert updated["name"] == "홍길순"

        deleted = delete_item(file_path, 100, id_field="user_no")
        assert deleted is True
        assert read_by_id(file_path, 100, id_field="user_no") is None

    print("test_crud_custom_id_field: PASS")


def run_all_tests():
    test_load_missing_file_raises()
    test_parse_invalid_json_raises()
    test_save_preserves_types_and_unicode()
    test_crud_missing_file_starts_empty()
    test_crud_id_reuse_after_delete()
    test_crud_update_does_not_add_unrelated_fields()
    test_crud_custom_id_field()
    print("모든 테스트 통과!")


if __name__ == "__main__":
    run_all_tests()
