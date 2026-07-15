# 오늘의 할 일 앱 - 개발 계획

## 기술 스택

### 백엔드
- **언어**: Python 3.11+
- **웹 프레임워크**: FastAPI
- **ORM**: SQLAlchemy 2.x
- **검증**: Pydantic
- **서버 실행**: Uvicorn

### 데이터베이스
- **DBMS**: SQLite
- **파일 경로**: .env 파일의 DATABASE_URL 환경변수로 관리
- **기본값**: sqlite:///./todos.db

### 프론트엔드
- **구조**: 단일 index.html 기반
- **템플릿 엔진**: Jinja2
- **스크립팅**: Vanilla JavaScript + fetch
- **빌드 도구**: 없음

### 테스트
- **프레임워크**: pytest
- **클라이언트**: FastAPI TestClient
- **검증 대상**: 생성/완료 토글/삭제/남은 개수/필터

---

## API 설계 (REST)

### 엔드포인트 명세

#### 1. 메인 화면
```
GET /
응답: HTML 페이지 (index.html)
목적: 프론트엔드 진입점
```

#### 2. 목록 조회
```
GET /api/todos?status={all|active|completed}
쿼리 파라미터: status (선택사항, 기본값: all)
응답 (200):
[
  {
    "id": 1,
    "title": "할 일 1",
    "completed": false,
    "created_at": "2024-01-01T00:00:00"
  },
  ...
]
```

#### 3. 할 일 생성
```
POST /api/todos
요청 본문:
{
  "title": "새 할 일"
}
응답 (201):
{
  "id": 1,
  "title": "새 할 일",
  "completed": false,
  "created_at": "2024-01-01T00:00:00"
}
에러 (422):
- 제목이 빈 문자열이거나 공백만 포함된 경우
- 응답: { "detail": [{"msg": "제목을 입력해주세요"}] }
```

#### 4. 할 일 부분 수정 (완료 토글)
```
PATCH /api/todos/{id}
요청 본문:
{
  "completed": true
}
응답 (200):
{
  "id": 1,
  "title": "할 일 1",
  "completed": true,
  "created_at": "2024-01-01T00:00:00"
}
에러 (404):
- 해당 ID의 할 일이 없는 경우
```

#### 5. 할 일 삭제
```
DELETE /api/todos/{id}
응답 (204): No Content
에러 (404):
- 해당 ID의 할 일이 없는 경우
```

#### 6. 상태 확인
```
GET /health
응답 (200):
{
  "status": "ok"
}
목적: 서버 헬스 체크
```

---

## 프로젝트 구조

```
vibe_sdd/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 라우터 및 앱 진입점
│   ├── database.py             # DB 세션 및 엔진 설정
│   ├── models.py               # SQLAlchemy ORM 모델
│   ├── schemas.py              # Pydantic 요청/응답 스키마
│   ├── crud.py                 # 데이터베이스 로직
│   └── templates/
│       └── index.html          # Jinja2 템플릿 기반 메인 화면
├── tests/
│   └── test_api.py             # API 테스트
├── .env                        # 환경 설정 (저장소 제외)
├── .env.example                # 환경 변수 예시
├── requirements.txt            # 의존성 목록
├── constitution.md             # 프로젝트 헌법
├── spec.md                     # 기능 명세서
├── plan.md                     # 개발 계획
├── research.md                 # 기술 조사 결과
├── data-model.md               # 데이터 모델
├── contracts/                  # API 계약 문서
│   └── todos-api.yaml
└── tasks.md                    # 구현 태스크 목록
```

---

## 동작 방식

### 초기 로드
1. 사용자가 브라우저에서 http://localhost:8000/에 접속한다.
2. FastAPI가 Jinja2 템플릿 기반 메인 화면을 렌더링해 반환한다.
3. 브라우저가 JavaScript를 로드해 API 호출을 시작한다.

### 데이터 로드
1. JavaScript가 페이지 로드 후 GET /api/todos?status=all을 호출한다.
2. 서버가 SQLite에서 할 일 목록을 조회해 JSON으로 응답한다.
3. JavaScript가 목록과 남은 개수를 다시 그린다.

### 사용자 작업
1. 사용자가 새 할 일을 입력하고 추가한다.
2. JavaScript가 POST /api/todos로 생성 요청을 보낸다.
3. 서버는 제목 검증 후 생성된 할 일을 반환한다.
4. JavaScript가 목록, 남은 개수, 필터 상태를 다시 렌더링한다.

### 페이지 새로고침 없는 업데이트
- 추가, 완료 토글, 삭제, 필터 변경은 모두 fetch로 처리한다.
- 서버 응답을 기준으로 화면을 즉시 갱신한다.
- 데이터는 SQLite에 저장되어 서버 재시작 후에도 유지된다.

---

## 개발 절차

### Phase 1: 백엔드 기초 (T01-T06)
1. DB 모델/스키마 구성
2. CRUD 로직 구현
3. API 엔드포인트 구현 (생성, 조회, 수정, 삭제)
4. 자동화 테스트 작성 및 검증

### Phase 2: 프론트엔드 (T07)
1. HTML 마크업 작성
2. CSS 스타일링 (반응형)
3. JavaScript 로직 작성
4. 수동 테스트 및 UI 검증

### Phase 3: 통합 테스트 (T08)
1. 전체 흐름 테스트
2. 데이터 영속성 검증
3. 반응형 디자인 검증

---

## 배포 및 실행

### 개발 환경 설정
```bash
# 1. 저장소 클론 후 디렉토리 이동
cd vibe_sdd

# 2. .env.example 복사
cp .env.example .env

# 3. 가상 환경 생성 및 활성화
python -m venv venv
source venv/Scripts/activate  # Windows
# 또는
source venv/bin/activate      # macOS/Linux

# 4. 의존성 설치
pip install -r requirements.txt

# 5. 테스트 실행
pytest tests/ -v

# 6. 서버 실행
uvicorn app.main:app --reload
```

### 접속
- 메인 페이지: `http://localhost:8000/`
- API 문서: `http://localhost:8000/docs`

---

## 주요 설계 결정

| 결정 사항 | 선택 | 이유 |
|---------|------|------|
| DB | SQLite | 단순성, 파일 기반 설정 용이 |
| 웹 프레임워크 | FastAPI | 빠른 성능, 자동 문서화, 타입 안정성 |
| ORM | SQLAlchemy 2.x | SQL 인젝션 방지, 타입 힌팅 지원 |
| 프론트엔드 | Vanilla JS + Jinja2 | 빌드 도구 불필요, 복잡도 낮음 |
| 테스트 | pytest | Python 표준, FastAPI 통합 용이 |
| 스타일링 | CSS3 | 프레임워크 의존 없음, 유지보수 용이 |

---

## 성능 고려사항

- **쿼리 최적화**: 필요시 인덱스 추가 (created_at, completed)
- **캐싱**: 할 일 목록은 자주 변경되므로 서버 캐싱 불필요
- **동시성**: SQLite는 쓰기 제약이 있으나, 단일 사용자 앱이므로 문제 없음

---

## 보안 고려사항

- **SQL 인젝션**: SQLAlchemy ORM 사용으로 자동 방지
- **CORS**: 현재 필요 없음 (같은 도메인에서 호출)
- **입력 검증**: Pydantic으로 자동 검증
- **HTTPS**: 로컬 개발이므로 현재 불필요
