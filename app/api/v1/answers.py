from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFound
from app.db.session import get_db
from app.schemas.answer import AnswerCreate, AnswerRead
from app.crud import answers as answers_crud

router = APIRouter()


@router.post(
    "/",
    response_model=AnswerRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer(
    answer_in: AnswerCreate,
    db: AsyncSession = Depends(get_db),
):
    answer = await answers_crud.create_answer(db, answer_in)
    if answer is None:
        raise NotFound("Question not found")
    return answer


@router.get(
    "/{answer_id}",
    response_model=AnswerRead,
)
async def get_answer(
    answer_id: int,
    db: AsyncSession = Depends(get_db),
):
    answer = await answers_crud.get_answer(db, answer_id)
    if answer is None:
        raise NotFound("Answer not found")
    return answer
