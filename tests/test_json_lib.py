"""json_lib 동작을 확인하는 간단한 테스트."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from json_lib import load_json, parse_json, save_json, to_json_string


def test_round_trip():
    """저장 후 다시 읽었을 때 원본 데이터와 동일한지 확인한다."""
    data = {
        "name": "테스트",
        "count": 3,
        "active": True,
        "items": [1, 2, 3],
        "nested": {"key": None},
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "sample.json"

        save_json(data, file_path)
        loaded = load_json(file_path)

        assert loaded == data, f"round-trip 실패: {loaded} != {data}"

    print("test_round_trip: PASS")


def test_parse_and_to_json_string():
    """문자열 파싱과 문자열 변환이 올바르게 동작하는지 확인한다."""
    text = '{"a": 1, "b": [true, false, null]}'
    parsed = parse_json(text)
    assert parsed == {"a": 1, "b": [True, False, None]}

    dumped = to_json_string(parsed)
    reparsed = parse_json(dumped)
    assert reparsed == parsed, "to_json_string 후 재파싱 결과가 다름"

    print("test_parse_and_to_json_string: PASS")


def run_all_tests():
    test_round_trip()
    test_parse_and_to_json_string()
    print("모든 테스트 통과!")


if __name__ == "__main__":
    run_all_tests()
