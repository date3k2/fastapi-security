from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class UserBase(SQLModel):
    username: str
    password: str


class Users(UserBase, table=True):
    userId: Optional[int] = Field(primary_key=True)
    loggedIn: int = Field(default=0)
    loggedAt: datetime = Field(default=None)
