from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import questions as questions_crud
from app.crud import answers as answers_crud
from app.core.exceptions import NotFound
from app.db.session import get_db
from app.schemas.question import QuestionCreate, QuestionRead
from app.schemas.answer import AnswerRead

router = APIRouter()


@router.post(
    "/",
    response_model=QuestionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_question(
    question_in: QuestionCreate,
    db: AsyncSession = Depends(get_db),
):
    question = await questions_crud.create_question(db, question_in)
    return question


@router.get(
    "/",
    response_model=List[QuestionRead],
)
async def list_questions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    questions = await questions_crud.list_questions(db, skip=skip, limit=limit)
    return questions


@router.get(
    "/{question_id}",
    response_model=QuestionRead,
)
async def get_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
):
    question = await questions_crud.get_question(db, question_id)
    if question is None:
        raise NotFound("Question not found")
    return question


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted = await questions_crud.delete_question(db, question_id)
    if not deleted:
        raise NotFound("Question not found")
    return None


@router.get(
    "/{question_id}/answers",
    response_model=List[AnswerRead],
)
async def list_answers_for_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
):
    question = await questions_crud.get_question(db, question_id)
    if question is None:
        raise NotFound("Question not found")

    answers = await answers_crud.list_answers_for_question(db, question_id)
    return answers
