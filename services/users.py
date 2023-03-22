from db.models import User
from db.database import engine
from sqlmodel import Session, SQLModel, select

def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_all_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
    return users