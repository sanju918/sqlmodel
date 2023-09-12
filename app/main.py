from fastapi import FastAPI

from app.api import users, generic, courses, sections
from app.db.db_setup import engine
from app.db.models import user, course

user.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)


def init_app():
    api_app = FastAPI(title="SQLModel Tutorial", description="Test", version="1")

    api_app.include_router(generic.router)
    api_app.include_router(users.router)
    api_app.include_router(courses.router)
    api_app.include_router(sections.router)

    return api_app


app = init_app()
