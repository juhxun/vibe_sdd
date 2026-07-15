# Tasks: 오늘의 할 일 웹 앱

**Input**: 설계 문서 /specs/001-todo-webapp/, /plan.md, /research.md, /data-model.md, /contracts/

**Organization**: 사용자 스토리 우선순위(P1 → P2) 기준으로 정렬하고, 각 태스크는 독립적으로 테스트 가능한 단위로 작성한다.

## Phase 1: Setup (공용 인프라)

**Purpose**: 기본 프로젝트 구조와 환경 설정

- [ ] T001 Create base project files and environment bootstrap in app/, tests/, and app/templates/index.html
  - 완료 조건: `app/__init__.py`, `app/main.py`, `app/models.py`, `app/schemas.py`, `app/crud.py`, `app/database.py`, `app/templates/index.html`, `tests/test_api.py` 파일이 생성되어 import 가능한 상태다.
- [ ] T002 Configure environment variables and database connection in app/database.py and .env.example
  - 완료 조건: `DATABASE_URL` 환경변수를 읽어 SQLite 연결을 만들고 `.env.example`에 문서화되어 있다.
- [ ] T003 [P] Add pytest fixtures and FastAPI TestClient setup in tests/test_api.py
  - 완료 조건: 테스트에서 `TestClient`를 사용해 앱을 기동할 수 있다.

---

## Phase 2: Foundational (블로킹 선행 작업)

**Purpose**: 사용자 스토리 구현 전에 반드시 완료해야 하는 기반 작업

- [ ] T004 Implement the Todo ORM model and database initialization in app/models.py and app/database.py
  - 완료 조건: `Todo` 테이블이 생성되고 `Base.metadata.create_all`로 초기화된다.
- [ ] T005 Implement Pydantic request and response schemas in app/schemas.py
  - 완료 조건: 빈 제목은 검증 오류로 거절되고 생성/응답 스키마가 정상 동작한다.
- [ ] T006 Implement CRUD helpers for list, create, update, and delete operations in app/crud.py
  - 완료 조건: 목록 조회, 생성, 완료 토글, 삭제, 미완료 개수 계산 함수가 모두 구현되어 있다.
- [ ] T007 Implement REST routes for GET /, GET /health, GET /api/todos, POST /api/todos, PATCH /api/todos/{id}, and DELETE /api/todos/{id} in app/main.py
  - 완료 조건: 기본 API 엔드포인트가 응답하고, `GET /health`가 `{"status":"ok"}`를 반환한다.

**Checkpoint**: 기본 API와 데이터 저장 경로가 준비되면 사용자 스토리 구현을 시작할 수 있다.

---

## Phase 3: User Story 1 - 새 할 일 추가 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 새 할 일을 추가하고 빈 입력을 거절할 수 있다.

**Independent Test**: POST /api/todos로 유효한 제목을 보내면 생성되고, 빈 제목은 422 응답을 받는지로 검증한다.

- [ ] T008 [P] [US1] Implement POST /api/todos creation flow in app/main.py and app/crud.py
  - 완료 조건: 유효한 제목으로 생성 요청 시 201 응답과 생성된 할 일이 반환된다.
- [ ] T009 [P] [US1] Add API tests for successful creation and empty-title rejection in tests/test_api.py
  - 완료 조건: `pytest tests/test_api.py -k "create"`가 통과한다.

---

## Phase 4: User Story 2 - 완료 상태 관리 및 토글 (Priority: P1)

**Goal**: 사용자가 할 일을 완료/미완료로 토글할 수 있다.

**Independent Test**: PATCH /api/todos/{id}로 completed 상태를 바꾸면 저장된 값이 바뀌고, 없는 ID는 404를 받는지로 검증한다.

- [ ] T010 [P] [US2] Implement PATCH /api/todos/{id} toggle logic in app/main.py and app/crud.py
  - 완료 조건: 완료 상태 변경이 저장되고, 존재하지 않는 ID는 404로 응답한다.
- [ ] T011 [P] [US2] Add API tests for toggle success and not-found behavior in tests/test_api.py
  - 완료 조건: `pytest tests/test_api.py -k "toggle or not_found"`가 통과한다.

---

## Phase 5: User Story 3 - 삭제, 필터, 남은 개수 (Priority: P2)

**Goal**: 사용자가 할 일을 삭제하고 필터와 남은 개수를 확인할 수 있다.

**Independent Test**: DELETE /api/todos/{id}와 GET /api/todos?status=all|active|completed가 올바르게 동작하는지로 검증한다.

- [ ] T012 [P] [US3] Implement DELETE /api/todos/{id} handling in app/main.py and app/crud.py
  - 완료 조건: 삭제된 항목은 더 이상 조회되지 않고, 없는 ID는 404를 반환한다.
- [ ] T013 [P] [US3] Implement status filtering and remaining-count logic in app/main.py and app/crud.py
  - 완료 조건: `all`, `active`, `completed` 필터가 각각 올바른 결과를 반환하고 남은 개수가 정확하다.
- [ ] T014 [P] [US3] Add API tests for delete, filtering, and remaining count in tests/test_api.py
  - 완료 조건: `pytest tests/test_api.py -k "delete or filter or remaining"`가 통과한다.

---

## Phase 6: User Story 4 - 화면(UI) 및 반응형 경험 (Priority: P2)

**Goal**: 사용자가 웹 화면에서 목록, 필터, 빈 상태, 삭제 확인, 반응형 레이아웃을 이용할 수 있다.

**Independent Test**: 메인 화면이 로드되고, 추가/토글/삭제/필터가 화면에 반영되며, 빈 상태 메시지가 표시되는지로 검증한다.

- [ ] T015 [US4] Create the main todo UI shell and responsive layout in app/templates/index.html
  - 완료 조건: 360px 폭에서도 주요 입력창, 목록, 필터, 버튼이 접근 가능하다.
- [ ] T016 [US4] Implement fetch-based add/toggle/delete/filter interactions and empty states in app/templates/index.html
  - 완료 조건: 페이지 새로고침 없이 목록과 남은 개수가 갱신되고 삭제 확인이 동작한다.
- [ ] T017 [US4] Add UI integration coverage for rendering and responsive behavior in tests/test_api.py
  - 완료 조건: UI 관련 시나리오가 테스트로 검증된다.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 통합 검증과 문서 보강

- [ ] T018 [P] Validate persistence across restart and health endpoint behavior in tests/test_api.py
  - 완료 조건: 서버 재시작 후 데이터가 유지되고 `/health`가 정상 상태를 반환한다.
- [ ] T019 [P] Review and align environment and usage documentation in README.md, .env.example, and plan.md
  - 완료 조건: 실행 방법과 환경 변수 설명이 최신 상태로 정리되어 있다.

---

## Dependencies & Execution Order

- Phase 1: No dependencies
- Phase 2: Depends on Phase 1
- Phase 3+: Depends on Phase 2
- UI work (Phase 6) depends on API completion from Phases 3–5

### Parallel Opportunities

- T003 can run in parallel with setup work
- T008 and T009 can be implemented in parallel
- T010 and T011 can be implemented in parallel
- T012, T013, and T014 can be implemented in parallel

### Implementation Strategy

1. Phase 1과 2를 먼저 완료해 기반 API를 만든다.
2. P1 작업(US1, US2)을 순차적으로 구현하고 테스트를 통과시킨다.
3. P2 작업(US3, US4)을 이어서 구현한다.
4. 마지막으로 통합 회귀 테스트와 문서 정리를 마친다.

**총 소요시간**: 약 6.5시간

---

## 주의사항

1. **스펙 준수**: spec.md에 없는 기능은 구현하지 않음
2. **테스트 우선**: 각 태스크 완료 후 테스트 통과 확인
3. **.env 관리**: 민감한 설정은 .env에만 저장, .env.example에 문서화
4. **커밋 메시지**: "T##:" 형식 준수
5. **한국어 문서**: 모든 문서는 한국어로 작성
