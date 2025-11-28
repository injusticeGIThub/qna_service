from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question import Question
from app.schemas.question import QuestionCreate


async def create_question(
    db: AsyncSession,
    obj_in: QuestionCreate,
) -> Question:
    question = Question(text=obj_in.text)
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question


async def get_question(
    db: AsyncSession,
    question_id: int,
) -> Optional[Question]:
    result = await db.execute(
        select(Question).where(Question.id == question_id)
    )
    return result.scalar_one_or_none()


async def list_questions(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[Question]:
    result = await db.execute(
        select(Question)
        .order_by(Question.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def delete_question(db: AsyncSession, question_id: int) -> bool:
    q = await db.execute(select(Question).where(Question.id == question_id))
    question = q.scalar_one_or_none()

    if not question:
        return False

    await db.delete(question)
    await db.commit()
    return True
