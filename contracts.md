# 오늘의 할 일 앱 - API 계약(Contract)

이 문서는 API의 요청/응답 명세서입니다. 프론트엔드와 백엔드 개발자가 함께 준수해야 합니다.

---

## 1. 메인 페이지

### 요청
```
GET /
헤더: Accept: text/html
```

### 응답
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
  ...
</html>
```

### 설명
- 프론트엔드 시작점
- Jinja2로 렌더링된 HTML 페이지 반환
- 초기 데이터는 JavaScript fetch로 별도 로드

---

## 2. 할 일 목록 조회

### 요청
```
GET /api/todos?status=all
GET /api/todos?status=active
GET /api/todos?status=completed
```

### 쿼리 파라미터
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|-------|------|
| `status` | string | 아니오 | `all` | 필터 종류 |

**status 값**:
- `all`: 모든 할 일
- `active`: 미완료 항목만 (`completed = false`)
- `completed`: 완료된 항목만 (`completed = true`)

### 응답 (200 OK)
```json
[
  {
    "id": 1,
    "title": "아침 운동",
    "completed": false,
    "created_at": "2024-01-01T08:00:00",
    "updated_at": "2024-01-01T08:00:00"
  },
  {
    "id": 2,
    "title": "회의 참석",
    "completed": true,
    "created_at": "2024-01-01T09:00:00",
    "updated_at": "2024-01-01T10:30:00"
  }
]
```

### 응답 (200 OK - 빈 목록)
```json
[]
```

### 응답 헤더
```
Content-Type: application/json
```

### 사용 예시 (JavaScript)
```javascript
// 모든 할 일 조회
fetch('/api/todos?status=all')
  .then(r => r.json())
  .then(todos => console.log(todos));

// 미완료 항목만 조회
fetch('/api/todos?status=active')
  .then(r => r.json())
  .then(todos => console.log(todos));
```

---

## 3. 할 일 생성

### 요청
```
POST /api/todos
Content-Type: application/json

{
  "title": "새 할 일"
}
```

### 요청 본문
| 필드 | 타입 | 필수 | 제약 | 설명 |
|------|------|------|------|------|
| `title` | string | 예 | 1~255자, 공백만 불가 | 할 일 제목 |

### 응답 (201 Created)
```json
{
  "id": 3,
  "title": "새 할 일",
  "completed": false,
  "created_at": "2024-01-01T11:00:00",
  "updated_at": "2024-01-01T11:00:00"
}
```

### 응답 헤더
```
Content-Type: application/json
Location: /api/todos/3
```

### 에러 응답 (422 Unprocessable Entity)
**케이스 1: 빈 제목**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "title"],
      "msg": "제목을 입력해주세요",
      "input": ""
    }
  ]
}
```

**케이스 2: 공백만 있는 제목**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "title"],
      "msg": "제목을 입력해주세요",
      "input": "   "
    }
  ]
}
```

**케이스 3: 제목 필드 누락**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "title"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

### 사용 예시 (JavaScript)
```javascript
const newTodo = { title: "할 일 입력" };

fetch('/api/todos', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(newTodo)
})
  .then(r => {
    if (r.ok) return r.json();
    if (r.status === 422) throw new Error('제목을 입력해주세요');
    throw new Error('서버 오류');
  })
  .then(todo => console.log('생성됨:', todo))
  .catch(err => console.error(err.message));
```

---

## 4. 할 일 부분 수정 (완료 토글)

### 요청
```
PATCH /api/todos/1
Content-Type: application/json

{
  "completed": true
}
```

### 요청 파라미터
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `id` (경로) | integer | 예 | 할 일 ID |

### 요청 본문
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `completed` | boolean | 예 | 완료 상태 |

### 응답 (200 OK)
```json
{
  "id": 1,
  "title": "아침 운동",
  "completed": true,
  "created_at": "2024-01-01T08:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### 응답 헤더
```
Content-Type: application/json
```

### 에러 응답 (404 Not Found)
```json
{
  "detail": "할 일을 찾을 수 없습니다"
}
```

### 에러 응답 (422 Unprocessable Entity)
**케이스: completed 필드 누락**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "completed"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

### 사용 예시 (JavaScript)
```javascript
const todoId = 1;

fetch(`/api/todos/${todoId}`, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ completed: true })
})
  .then(r => {
    if (r.ok) return r.json();
    if (r.status === 404) throw new Error('할 일을 찾을 수 없습니다');
    throw new Error('서버 오류');
  })
  .then(todo => console.log('수정됨:', todo))
  .catch(err => console.error(err.message));
```

---

## 5. 할 일 삭제

### 요청
```
DELETE /api/todos/1
```

### 요청 파라미터
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `id` (경로) | integer | 예 | 할 일 ID |

### 응답 (204 No Content)
```
(본문 없음)
```

### 에러 응답 (404 Not Found)
```json
{
  "detail": "할 일을 찾을 수 없습니다"
}
```

### 사용 예시 (JavaScript)
```javascript
const todoId = 1;

fetch(`/api/todos/${todoId}`, {
  method: 'DELETE'
})
  .then(r => {
    if (r.ok) return Promise.resolve();
    if (r.status === 404) throw new Error('할 일을 찾을 수 없습니다');
    throw new Error('서버 오류');
  })
  .then(() => console.log('삭제됨'))
  .catch(err => console.error(err.message));
```

---

## 6. 상태 확인 (헬스 체크)

### 요청
```
GET /health
```

### 응답 (200 OK)
```json
{
  "status": "ok"
}
```

### 용도
- 서버 가동 여부 확인
- 로드 밸런서 헬스 체크

---

## HTTP 상태 코드 정리

| 코드 | 의미 | 사용 사례 |
|------|------|---------|
| `200 OK` | 성공 | 조회, 수정 완료 |
| `201 Created` | 생성 성공 | 할 일 생성 완료 |
| `204 No Content` | 성공 (응답 본문 없음) | 삭제 완료 |
| `404 Not Found` | 리소스 없음 | 존재하지 않는 할 일 |
| `422 Unprocessable Entity` | 검증 실패 | 빈 제목, 잘못된 필드 |
| `500 Internal Server Error` | 서버 오류 | 예상 밖의 오류 |

---

## 데이터 타입 명세

### 타임스탬프
- 형식: ISO 8601 (RFC 3339)
- 예: `2024-01-01T08:00:00`
- 시간대: UTC
- JavaScript에서 파싱: `new Date("2024-01-01T08:00:00")`

### Boolean
- `true` 또는 `false` (JSON 형식)
- JavaScript에서 비교: `if (todo.completed) { ... }`

### 정수
- 부호 있는 정수 (-2147483648 ~ 2147483647)
- 예: `"id": 1`

### 문자열
- UTF-8 인코딩
- 최대 길이: 255자 (title)
- 개행 제거: 클라이언트에서 `.trim()` 권장

---

## CORS 정책 (향후)

현재 필요 없음. 향후 다른 도메인에서 호출할 경우 추가 필요.

```python
# app/main.py (향후 추가)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 레이트 제한 (향후)

현재 필요 없음. 향후 공개 API로 전환할 경우 추가 필요.

---

## 버전 관리 (향후)

현재: v1 (암시적)
향후: `/api/v2/todos` 등으로 명시적 버전 관리

---

## 보안 헤더 (향후)

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
```

---

## 예시 완전한 흐름

### 1단계: 할 일 조회
```bash
curl http://localhost:8000/api/todos?status=all
# 응답: []
```

### 2단계: 할 일 생성
```bash
curl -X POST http://localhost:8000/api/todos \
  -H 'Content-Type: application/json' \
  -d '{"title":"할 일 1"}'
# 응답: {"id":1,"title":"할 일 1","completed":false,...}
```

### 3단계: 다시 목록 조회
```bash
curl http://localhost:8000/api/todos?status=all
# 응답: [{"id":1,"title":"할 일 1","completed":false,...}]
```

### 4단계: 완료 토글
```bash
curl -X PATCH http://localhost:8000/api/todos/1 \
  -H 'Content-Type: application/json' \
  -d '{"completed":true}'
# 응답: {"id":1,"title":"할 일 1","completed":true,...}
```

### 5단계: 미완료 항목만 조회
```bash
curl http://localhost:8000/api/todos?status=active
# 응답: []
```

### 6단계: 완료된 항목 조회
```bash
curl http://localhost:8000/api/todos?status=completed
# 응답: [{"id":1,"title":"할 일 1","completed":true,...}]
```

### 7단계: 삭제
```bash
curl -X DELETE http://localhost:8000/api/todos/1
# 응답: (204 No Content)
```
