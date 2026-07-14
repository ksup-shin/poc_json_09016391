"""json_crud CRUD 동작을 확인하는 간단한 테스트."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from json_crud import create_item, read_all, read_by_id, update_item, delete_item


def test_create_and_read():
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "data.json"

        create_item(file_path, {"id": 1, "name": "사과", "price": 1000})
        create_item(file_path, {"id": 2, "name": "바나나", "price": 500})

        all_items = read_all(file_path)
        assert len(all_items) == 2

        found = read_by_id(file_path, 1)
        assert found == {"id": 1, "name": "사과", "price": 1000}

        not_found = read_by_id(file_path, 999)
        assert not_found is None

    print("test_create_and_read: PASS")


def test_create_duplicate_id_fails():
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "data.json"

        create_item(file_path, {"id": 1, "name": "사과"})
        try:
            create_item(file_path, {"id": 1, "name": "복숭아"})
            assert False, "중복 id 생성이 예외 없이 통과했다"
        except ValueError:
            pass

    print("test_create_duplicate_id_fails: PASS")


def test_update():
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "data.json"

        create_item(file_path, {"id": 1, "name": "사과", "price": 1000})

        updated = update_item(file_path, 1, {"price": 1200})
        assert updated == {"id": 1, "name": "사과", "price": 1200}

        # id 필드는 수정되지 않아야 한다.
        updated_again = update_item(file_path, 1, {"id": 999, "name": "청사과"})
        assert updated_again["id"] == 1
        assert updated_again["name"] == "청사과"

        missing = update_item(file_path, 42, {"name": "없음"})
        assert missing is None

    print("test_update: PASS")


def test_delete():
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "data.json"

        create_item(file_path, {"id": 1, "name": "사과"})
        create_item(file_path, {"id": 2, "name": "바나나"})

        result = delete_item(file_path, 1)
        assert result is True
        assert read_by_id(file_path, 1) is None
        assert len(read_all(file_path)) == 1

        # 이미 없는 항목을 삭제해도 예외 없이 False.
        result_again = delete_item(file_path, 1)
        assert result_again is False

    print("test_delete: PASS")


def run_all_tests():
    test_create_and_read()
    test_create_duplicate_id_fails()
    test_update()
    test_delete()
    print("모든 테스트 통과!")


if __name__ == "__main__":
    run_all_tests()
