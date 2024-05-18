from typing import List, Optional
from pydantic import BaseModel
from datetime import timedelta


class User(BaseModel):
    """
    User class containing information on users, will be used to store users in a DB
    """
    username: str
    email: str = None
    hashed_password: str
    disabled: bool = False


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    time_remaining: Optional[timedelta] = None
    status: str