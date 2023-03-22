from db.models import Loan
from db.database import engine
from sqlmodel import Session, SQLModel, select

def create_loan(loan: Loan):
    with Session(engine) as session:
        session.add(loan)
        session.commit()
        session.refresh(loan)
        return loan


def get_all_loans():
    with Session(engine) as session:
        users = session.exec(select(Loan)).all()
    return users