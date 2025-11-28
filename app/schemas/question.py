from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class QuestionBase(BaseModel):
    text: str

    @field_validator("text")
    def validate_text(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Question text cannot be empty")
        if len(v) > 2000:
            raise ValueError("Question text is too long (max 2000 chars)")
        return v


class QuestionCreate(QuestionBase):
    """Схема для создания вопроса."""
    pass


class QuestionRead(QuestionBase):
    """Схема для возврата вопроса."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionListItem(QuestionRead):
    """Список вопросов"""
    pass
