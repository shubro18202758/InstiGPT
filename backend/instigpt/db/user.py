from typing import Optional

from sqlmodel import SQLModel, Field, Session, select, insert

from . import get_engine


class User(SQLModel, table=True):
    id: int = Field(primary_key=True, description="The ID of the user (from gymkhana)")
    username: str = Field(description="The username of the user (from gymkhana)")
    name: str = Field(description="The name of the user (from gymkhana)")
    email: str = Field(description="The email of the user (from gymkhana)")
    roll_number: str = Field(description="The roll number of the user (from gymkhana)")


def get_user_by_id(id: int) -> Optional[User]:
    with Session(get_engine()) as session:
        statement = select(User).where(User.id == id)
        user = session.exec(statement).first()

    return user


def create_user(user: User):
    with Session(get_engine(), expire_on_commit=False) as session:
        session.add(user)
        session.commit()
