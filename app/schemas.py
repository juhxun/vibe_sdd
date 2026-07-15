"""
Pydantic 요청/응답 스키마
"""
from datetime import datetime
from pydantic import BaseModel, field_validator


class TodoCreate(BaseModel):
    """할 일 생성 요청"""

    title: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("제목을 입력해주세요")
        return v.strip()


class TodoUpdate(BaseModel):
    """할 일 수정 요청"""

    completed: bool


class TodoResponse(BaseModel):
    """할 일 응답"""

    id: int
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
