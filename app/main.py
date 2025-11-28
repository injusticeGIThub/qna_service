from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import questions, answers
from app.core.error_handler import app_exception_handler, validation_exception_handler
from app.core.exceptions import AppException
from app.db.session import get_db


app = FastAPI(
    title="Q&A API",
    version="0.1.0",
)

# exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# routers
app.include_router(questions.router, prefix="/questions", tags=["questions"])
app.include_router(answers.router, prefix="/answers", tags=["answers"])


@app.get("/", tags=["health"])
def read_root() -> dict:
    return {"status": "OK"}


@app.get("/db-check", tags=["health"])
async def db_check(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    value = result.scalar_one()
    return {"db": "OK", "result": value}
