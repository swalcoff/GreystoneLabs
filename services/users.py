from db.models import User
from db.database import engine
from sqlmodel import Session, SQLModel, select
from fastapi import HTTPException

def create_user(user: User):
    with Session(engine) as session:
        users = session.exec(select(User).where(User.id == user.id)).all()
        if len(users) > 0:
            raise HTTPException(status_code=409, detail=f"User with ID {user.id} already exists")
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"message": f"User with ID {user.id} has been created successfully"}


def get_all_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
    return users