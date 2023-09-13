import fastapi
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db_setup import get_db
from app.pydantic_schemas.course_schema import Course, CourseCreate
from app.api.utils.courses_crud import get_course, get_courses, create_course

router = fastapi.APIRouter()
tag = ["Courses"]

db: Session = Depends(get_db)


@router.get("/courses", tags=tag, response_model=List[Course])
async def read_courses(db_=db):
    res = get_courses(db_)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return res


@router.post("/courses", tags=tag, response_model=Course)
async def create_new_course(course: CourseCreate, db_=db):
    return create_course(db=db_, course=course)


@router.get("/courses/{course_id}", tags=tag)
async def read_course(course_id: int, db_=db):
    res = get_course(db=db_, course_id=course_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested course do not exist.")
    return get_course(db=db_, course_id=course_id)


@router.patch("/courses", tags=tag)
async def update_course(course: CourseCreate, db_=db):
    return create_course(db=db_, course=course)


@router.delete("/courses/{id}", tags=tag)
async def delete_course():
    return {"courses": []}


@router.get("/courses/{id}/sections", tags=tag)
async def read_course_sections():
    return {"courses": []}