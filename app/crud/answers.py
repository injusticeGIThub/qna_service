from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.answer import Answer
from app.models.question import Question
from app.schemas.answer import AnswerCreate


async def create_answer(
    db: AsyncSession,
    obj_in: AnswerCreate,
) -> Optional[Answer]:
    q = await db.execute(
        select(Question).where(Question.id == obj_in.question_id)
    )
    question = q.scalar_one_or_none()
    if question is None:
        return None

    answer = Answer(
        question_id=obj_in.question_id,
        user_id=obj_in.user_id,
        text=obj_in.text,
    )
    db.add(answer)
    await db.commit()
    await db.refresh(answer)
    return answer


async def get_answer(
    db: AsyncSession,
    answer_id: int,
) -> Optional[Answer]:
    result = await db.execute(
        select(Answer).where(Answer.id == answer_id)
    )
    return result.scalar_one_or_none()


async def list_answers_for_question(
    db: AsyncSession,
    question_id: int,
) -> List[Answer]:
    result = await db.execute(
        select(Answer)
        .where(Answer.question_id == question_id)
        .order_by(Answer.created_at.asc())
    )
    return list(result.scalars().all())
