import fastapi
from fastapi import Path, Query
from api.models.user_model import User
import uuid
from typing import List, Optional

router = fastapi.APIRouter()

users = [{
    "id": 5423142523,
    "email": "sanjaypatel@walmart.com",
    "is_active": False
  }]


@router.get("/user", response_model=List[User])
async def get_users():
    return users


@router.post("/user")
async def create_user(user: User):
    user.id = uuid.uuid4().int % (10 ** 10)
    users.append(user)
    return {"message": "created user"}


@router.get("/users/{user_id}", response_model=Optional[dict])
async def get_user(
        user_id: int = Path(..., description="The ID of the user", gt=0),
        q: bool = Query(False)
):
    for user in users:
        if user["id"] == user_id and user["is_active"] == q:
            return {"user": user, "query": q}
