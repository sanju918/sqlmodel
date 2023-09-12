from sqlmodel import Field, SQLModel
from typing import Optional


class Hero(SQLModel, table=True):
    # id we set optional coz database will add value for this field
    id: Optional[int] = Field(default=None, primary_key=True)  # To set it as PK we need special function Field
    name: str
    secret_name: str
    age: Optional[int] = None  # Optional[int] is same as Union[int, None]
    sex: Optional[str] = None


class User(SQLModel, table=True):
    userid: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Optional[str]
    super_user: bool
    active_user: bool


class TestTable(SQLModel, table=True):
    test_id: Optional[int] = Field(default=None, primary_key=True)
