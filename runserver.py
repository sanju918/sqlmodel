from fastapi import FastAPI
import uvicorn
from api import generic, users


def init_app():
    api_app = FastAPI(title="SQLModel Tutorial", description="Test", version="1")

    return api_app


app = init_app()
app.include_router(generic.router)
app.include_router(users.router)


def start():
    uvicorn.run("runserver:app", host="localhost", port=8080, reload=True)


if __name__ == "__main__":
    start()
