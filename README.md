# PoC_Json

JSON 파일을 읽고 쓰기 위한 간단한 파이썬 라이브러리. 두 개의 모듈로 구성된다.

- `json_lib.py` — JSON 파싱/저장 기본 기능
- `json_crud.py` — `json_lib`을 기반으로 한 CRUD(Create/Read/Update/Delete) 기능

## 설치

외부 의존성 없이 파이썬 표준 라이브러리(`json`, `pathlib`)만 사용한다. `json_lib.py`와 `json_crud.py` 파일을 프로젝트에 복사하거나, 이 저장소를 그대로 import 경로에 두면 된다.

```python
from json_lib import load_json, save_json, parse_json, to_json_string
from json_crud import create_item, read_all, read_by_id, update_item, delete_item
```

## json_lib — 기본 파싱/저장

| 함수 | 설명 |
| --- | --- |
| `load_json(file_path)` | JSON 파일을 읽어 파이썬 객체로 반환 |
| `parse_json(text)` | JSON 문자열을 파이썬 객체로 파싱 |
| `save_json(data, file_path, indent=2, ensure_ascii=False)` | 파이썬 객체를 JSON 파일로 저장 |
| `to_json_string(data, indent=2, ensure_ascii=False)` | 파이썬 객체를 JSON 문자열로 변환 |

```python
from json_lib import load_json, save_json

data = load_json("config.json")
data["version"] = "1.1"
save_json(data, "config.json")
```

- `save_json`은 대상 폴더가 없으면 자동으로 생성한다.
- `ensure_ascii=False`가 기본값이라 한글 등 비ASCII 문자가 그대로 저장된다.

## json_crud — 레코드 CRUD

JSON 파일 하나를 "레코드 목록"으로 다룬다. 파일 내용은 각 레코드(dict)의 리스트이며, 각 레코드는 고유한 `id` 필드를 가져야 한다.

```json
[
  { "id": 1, "name": "사과", "price": 1000 },
  { "id": 2, "name": "바나나", "price": 500 }
]
```

### Create

```python
from json_crud import create_item

create_item("items.json", {"id": 1, "name": "사과", "price": 1000})
```

- 파일이 없으면 새로 만든다.
- 같은 `id` 값이 이미 있으면 `ValueError`가 발생한다.

### Read

```python
from json_crud import read_all, read_by_id

all_items = read_all("items.json")          # 전체 목록
item = read_by_id("items.json", 1)          # id=1 검색, 없으면 None
```

### Update

```python
from json_crud import update_item

update_item("items.json", 1, {"price": 1200})
```

- 지정한 필드만 수정되고 나머지 필드는 그대로 유지된다.
- `id` 필드는 수정 대상에서 제외되어 실수로 바뀌지 않는다.
- 대상 id가 없으면 아무것도 수정하지 않고 `None`을 반환한다.

### Delete

```python
from json_crud import delete_item

deleted = delete_item("items.json", 1)      # 성공 시 True, 대상 없으면 False
```

- 삭제 전 대상 존재 여부를 확인하므로 없는 id를 지워도 예외 없이 `False`만 반환한다(안전한 삭제).

### id 필드 이름 바꾸기

기본 키 이름은 `"id"`이며, 모든 CRUD 함수는 `id_field` 인자로 다른 키 이름을 쓸 수 있다.

```python
create_item("users.json", {"user_no": 100, "name": "홍길동"}, id_field="user_no")
read_by_id("users.json", 100, id_field="user_no")
```

## 테스트

각 모듈에 대응하는 테스트 스크립트가 있으며, 별도 테스트 프레임워크 없이 바로 실행할 수 있다.

```bash
python test_json_lib.py
python test_json_crud.py
```

정상 동작 시 각 테스트 이름과 함께 `PASS`, 마지막에 `모든 테스트 통과!`가 출력된다.
