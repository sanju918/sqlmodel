import fastapi
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app.db.db_setup import get_db
from app.api.utils.users_crud import get_user, get_user_by_email, get_users, create_user
from app.api.utils.courses_crud import get_user_courses
from app.pydantic_schemas.user_schema import User, UserCreate
from app.pydantic_schemas.course_schema import Course

router = fastapi.APIRouter()
db_: Session = Depends(get_db)


@router.get("/user", response_model=List[User], tags=["User"])
async def read_users(skip: int = 0, limit: int = 100, db=db_):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.post("/users", tags=["User"], response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db=db_):
    db_user = get_user_by_email(db, email=user.email, )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Provided Email is not available for use."
        )
    return create_user(db, user=user)


@router.get("/users/{user_id}", tags=["User"])
async def read_user(user_id: int, db=db_):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} doesn't exist."
        )

    return db_user


@router.get("/users/{user_id}/courses", response_model=List[Course], tags=["User", "Courses"])
async def read_user_courses(user_id: int, db=db_):
    courses = get_user_courses(db=db, user_id=user_id)
    if not courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records for selected user")
    return courses
