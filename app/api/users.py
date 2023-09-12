import fastapi
from fastapi import Path, Query
from app.api.models.user_model import User
from typing import List, Optional

router = fastapi.APIRouter()

users = [
    {
        "email": "sanjaypatel@walmart.com",
        "is_active": True,
        "bio": "I'm a software engineer"
    },
    {
        "email": "bindiyapatel@walmart.com",
        "is_active": False,
        "bio": "I'm home maker"
    }
]


@router.get("/user", response_model=List[User], tags=["User"])
async def get_users():
    return users


@router.post("/user", tags=["User"])
async def create_user(user: User):
    users.append(user)
    return {"message": "created user"}


@router.get("/users/{user_id}", response_model=Optional[dict], tags=["User"])
async def get_user(
        user_id: int = Path(..., description="The ID of the user", gt=0, le=2),
        q: str = Query(max_length=5)
):
    return { "user": users[user_id], "Query": q}
