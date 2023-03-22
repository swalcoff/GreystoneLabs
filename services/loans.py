from db.models import Loan, Loan_Summary
from db.database import engine
from sqlmodel import Session, SQLModel, select

def create_loan(loan: Loan):

    with Session(engine) as session:
        session.add(loan)
        session.commit()
        session.refresh(loan)
    schedule = []
    balance = loan.principle
    total_interest = 0
    for m in range(1, loan.term+1):
        int_payment = round((balance * (loan.apr * .01))/12, 2)
        pri_payment = loan.monthly_payment - int_payment
        balance -= pri_payment
        total_interest += int_payment
        l = Loan_Summary(loanid=loan.id, month=m, balance=balance, payment=loan.monthly_payment, principle=pri_payment, interest=int_payment, total_interest=total_interest)
        schedule.append(l)
    
    with Session(engine) as session:
        for month in schedule:
            session.add(month)
            session.commit()
    
    return loan


def get_all_loans():
    with Session(engine) as session:
        users = session.exec(select(Loan)).all()
    return users