"""tests 디렉토리의 모든 테스트를 한 번에 실행한다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import test_json_lib
import test_json_crud
import test_regression


def main():
    test_json_lib.run_all_tests()
    test_json_crud.run_all_tests()
    test_regression.run_all_tests()
    print("전체 테스트 스위트 통과!")


if __name__ == "__main__":
    main()
