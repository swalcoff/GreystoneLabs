from db.models import Loan, Loan_Summary, LoanCreate, User_Loan, User
from db.database import engine
from sqlmodel import Session, SQLModel, select, and_
from fastapi import HTTPException

def create_loan(loan_create: LoanCreate):
    if loan_create.apr < 0:
        raise HTTPException(status_code=400, detail="APR cannot be negative")
    if loan_create.term <= 0:
        raise HTTPException(status_code=400, detail="Loan Term must be greater than 0")
    if loan_create.principle <= 0:
        raise HTTPException(status_code=400, detail="Principle must be greater than 0")
    loan = Loan.from_orm(loan_create)
    rate = (loan.apr * 0.01)/12
    monthly = loan.principle * ((rate * pow(1+rate, loan.term))/(pow(1+rate, loan.term)-1))
    monthly = round(monthly, 2)
    loan.monthly_payment = monthly
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == loan_create.userid)).all()
        if len(user)==0:
            raise HTTPException(status_code=404, detail=f"User ID {loan_create.userid} not found. Please use existing User ID")
        l = session.exec(select(Loan).where(Loan.id == loan_create.id)).all()
        if len(l) > 0:
            raise HTTPException(status_code=409, detail=f"Loan with ID {loan_create.id} already exists")
        session.add(loan)
        session.commit()
        session.refresh(loan)
        balance = loan.principle
        total_interest = 0
        total_pri = 0
        for m in range(1, loan.term+1):
            int_payment = round((balance * (loan.apr * .01))/12, 2)
            pri_payment = round(monthly - int_payment, 2)
            balance = round(balance - pri_payment, 2)
            total_interest = round(total_interest + int_payment, 2)
            total_pri = round(total_pri + pri_payment, 2)
            session.add(Loan_Summary(loanid=loan.id, month=m, balance=balance, payment=monthly, principle=pri_payment, interest=int_payment, total_interest=total_interest, total_principle=total_pri))
        session.commit()
    
    # with Session(engine) as session:
    #     for month in schedule:
    #         session.add(month)
    #         session.commit()
        
        m2m = User_Loan(userid=loan_create.userid, loanid=loan.id)
        session.add(m2m)
        session.commit()

        return {"message": f"Loan with ID {loan.id} has been created successfully"}


def get_all_loans():
    with Session(engine) as session:
        users = session.exec(select(Loan)).all()
    return users

def get_loan_schedule(loan_id: int):
    with Session(engine) as session:
        loan_schedules = session.exec(select(Loan_Summary).where(Loan_Summary.loanid == loan_id)).all()
        if len(loan_schedules) == 0:
            raise HTTPException(status_code=404, detail=f"Loan with ID {loan_id} not found")
        return loan_schedules

def get_loan_summary(loan_id: int, month: int):
    with Session(engine) as session:
        loan_summary = session.exec(select(Loan_Summary).where(and_(Loan_Summary.month == month, Loan_Summary.loanid == loan_id))).all()
        if len(loan_summary) == 0:
            raise HTTPException(status_code=404, detail=f"Loan summary not found: Loan with ID {loan_id} does not exist")
        loan = session.exec(select(Loan).where(Loan.id == loan_id)).first()
        if loan.term < month:
            raise HTTPException(status_code=404, detail=f"Loan summary not found: Month {month} exceeds loan term")
    return loan_summary[0]

def get_user_loans(user_id: int):
    with Session(engine) as session:
        users = session.exec(select(User).where(User.id == user_id)).all()
        if len(users) == 0:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        m2m = session.exec(select(User_Loan).where(User_Loan.userid == user_id)).all()
        if len(m2m) == 0:
            raise HTTPException(status_code=404, detail=f"Loans for user with ID {user_id} not found")
        loans = []
        for mapping in m2m:
            loan = session.exec(select(Loan).where(Loan.id == mapping.loanid)).all()
            loans += loan
    return loans

def share_loan(user_id:int, loan_id:int):
    with Session(engine) as session:
        loans = session.exec(select(Loan).where(Loan.id == loan_id)).all()
        if len(loans)==0:
            raise HTTPException(status_code=404, detail=f"Loan ID {loan_id} not found")
        users = session.exec(select(User).where(User.id == user_id)).all()
        if len(users)==0:
            raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")
        shared = session.exec(select(User_Loan).where(and_(User_Loan.userid == user_id, User_Loan.loanid == loan_id))).all()
        if len(shared) > 0:
            raise HTTPException(status_code=409, detail=f"User ID {user_id} is already on loan with ID {loan_id}")
        ul = User_Loan(userid=user_id, loanid=loan_id)
        session.add(ul)
        session.commit()
        session.refresh(ul)

    return {"message": f"User with ID {user_id} has successfully been added to loan with ID {loan_id}"}