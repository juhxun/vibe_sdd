# 오늘의 할 일 앱 - 데이터 모델

## 데이터베이스 스키마

### Todo 테이블

| 컬럼명 | 타입 | 제약 | 설명 |
|---------|------|------|------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | 할 일 고유 식별자 |
| `title` | VARCHAR(255) | NOT NULL | 할 일 제목 |
| `completed` | BOOLEAN | NOT NULL, DEFAULT=false | 완료 여부 |
| `created_at` | DATETIME | NOT NULL, DEFAULT=CURRENT_TIMESTAMP | 생성 시간 |
| `updated_at` | DATETIME | NOT NULL, DEFAULT=CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | 수정 시간 |

---

## SQLAlchemy ORM 모델

```python
# app/models.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

---

## Pydantic 스키마

### TodoBase (공통 필드)
```python
class TodoBase(BaseModel):
    title: str
    completed: bool = False
```

### TodoCreate (생성 요청)
```python
class TodoCreate(BaseModel):
    title: str
    
    @field_validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('제목을 입력해주세요')
        return v.strip()
```

### TodoUpdate (수정 요청)
```python
class TodoUpdate(BaseModel):
    completed: bool
```

### TodoResponse (응답)
```python
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

---

## 인덱스 설계

### 현재 인덱스
- `id` (PRIMARY KEY)
- `created_at` (검색 성능 최적화 용)
- `completed` (필터링 성능 최적화 용)

### 복합 인덱스 (향후)
```sql
CREATE INDEX idx_completed_created ON todos(completed, created_at DESC);
```
> 필터링 + 정렬 성능이 필요해지면 추가

---

## 데이터 관계

### Todo 간 관계
- 현재: 관계 없음 (1단일 엔티티)
- 향후 확장: 사용자 인증 추가 시 User 테이블과 외래키 연결

---

## 데이터 무결성 제약

| 제약 | 규칙 | 이유 |
|-----|------|------|
| `NOT NULL (title)` | 제목은 항상 존재해야 함 | 의미있는 할 일 | 
| `NOT NULL (completed)` | 완료 상태는 항상 정의됨 | 기본값=false |
| `NOT NULL (created_at)` | 생성 시간은 항상 기록 | 감사 추적 |
| `DEFAULT (created_at)` | 자동으로 현재 시간 기록 | 일관성 보장 |
| `ON UPDATE (updated_at)` | 수정 시 자동 갱신 | 변경 추적 |

---

## 마이그레이션 전략

### 초기화 (app/database.py)
```python
from app.database import Base, engine
from app.models import Todo

# 앱 시작 시 테이블 자동 생성
Base.metadata.create_all(bind=engine)
```

### 향후 마이그레이션
- Alembic 도구 도입 예정 (필요시)
- 현재: 개발 환경에서 간단한 재생성으로 충분

---

## 쿼리 패턴

### 모든 할 일 조회 (정렬: 생성일 역순)
```python
db.query(Todo).order_by(Todo.created_at.desc()).all()
```

### 미완료 항목만 조회
```python
db.query(Todo).filter(Todo.completed == False).order_by(Todo.created_at.desc()).all()
```

### 완료된 항목만 조회
```python
db.query(Todo).filter(Todo.completed == True).order_by(Todo.created_at.desc()).all()
```

### ID로 할 일 조회
```python
db.query(Todo).filter(Todo.id == todo_id).first()
```

### 미완료 항목 개수
```python
db.query(Todo).filter(Todo.completed == False).count()
```

---

## 데이터 예시

### 초기 상태
```
(빈 테이블)
```

### 할 일 3개 추가 후
```
| id | title | completed | created_at | updated_at |
|----|-------|-----------|------------|------------|
| 1  | 아침 운동 | false | 2024-01-01 08:00:00 | 2024-01-01 08:00:00 |
| 2  | 회의 참석 | true  | 2024-01-01 09:00:00 | 2024-01-01 10:30:00 |
| 3  | 코드 리뷰 | false | 2024-01-01 10:00:00 | 2024-01-01 10:00:00 |
```

### 미완료 개수 조회
```
결과: 2 (1번, 3번)
```

---

## 동시성 고려사항

### 현재 (SQLite + 단일 서버)
- 동시 쓰기 제약: SQLite는 한 번에 하나의 쓰기만 허용
- 영향: 매우 낮음 (단일 사용자, 단일 프로세스)
- 타임아웃: 기본 5초 (충분함)

### 향후 (PostgreSQL 등으로 마이그레이션)
- ORM은 변경 없음 (SQLAlchemy 추상화)
- 연결 문자열만 변경: `sqlite:///` → `postgresql://`
