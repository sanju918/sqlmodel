from pydantic import BaseModel
from typing import Optional, Union
from sqlmodel import Field


class User(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    is_active: bool = False
