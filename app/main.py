from fastapi import FastAPI

from app.api import users_router, generic_router, courses_router, sections_router
from app.db.db_setup import engine
from app.db.models import user_model, course_model

user_model.Base.metadata.create_all(bind=engine)
course_model.Base.metadata.create_all(bind=engine)


def init_app():
    api_app = FastAPI(title="SQLModel Tutorial", description="Test", version="1")

    api_app.include_router(generic_router.router)
    api_app.include_router(users_router.router)
    api_app.include_router(courses_router.router)
    api_app.include_router(sections_router.router)

    return api_app


app = init_app()
