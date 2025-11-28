from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class AnswerBase(BaseModel):
    question_id: int
    user_id: str
    text: str

    @field_validator("text")
    def validate_text(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Answer text cannot be empty")
        if len(v) > 2000:
            raise ValueError("Answer text is too long (max 2000 chars)")
        return v

    @field_validator("user_id")
    def validate_user_id(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("user_id cannot be empty")
        if len(v) > 64:
            raise ValueError("user_id exceeds max length (64)")
        return v

    @field_validator("question_id")
    def validate_question_id(cls, v: int):
        if v <= 0:
            raise ValueError("question_id must be positive")
        return v


class AnswerCreate(AnswerBase):
    """Схема для создания ответа."""
    pass


class AnswerRead(AnswerBase):
    """Схема для возврата ответа наружу."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
