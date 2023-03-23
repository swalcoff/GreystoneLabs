from db.models import User, Loan, LoanCreate, Loan_Summary, Loan_Summary_Read, Loan_Schedule_Read
from db.database import engine, create_db_and_tables
from sqlmodel import Field, Session, SQLModel, create_engine, select
import services.users as UserService
import services.loans as LoanService
from fastapi import FastAPI, Path
from typing import List

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/users", response_model=List[User])
def get_all_users():
    return UserService.get_all_users()

@app.post("/users", response_model=dict)
def create_user(user: User):
    return UserService.create_user(user)

@app.get("/loans", response_model=List[Loan])
def get_all_loans():
    return LoanService.get_all_loans()

@app.post("/loans", response_model=dict)
def create_loan(loan: LoanCreate):
    return LoanService.create_loan(loan)

@app.get("/loan_schedule/{loan_id}", response_model=List[Loan_Schedule_Read])
def get_loan_schedule(loan_id: int = Path(None, description="The ID of the loan you want to get the schedule for")):
    return LoanService.get_loan_schedule(loan_id)

@app.get("/loan_summary/{loan_id}", response_model=Loan_Summary_Read)
def get_loan_summary(*, loan_id: int,month: int):
    return LoanService.get_loan_summary(loan_id=loan_id, month=month)

@app.get("/loans/{user_id}", response_model=List[Loan])
def get_user_loans(user_id: int = Path(None, description="ID of user for whom you'd like to fetch loans")):
    return LoanService.get_user_loans(user_id)

@app.get("/share_loan", response_model=dict)
def share_loan(*, user_id:int, loan_id:int):
    return LoanService.share_loan(user_id=user_id, loan_id=loan_id)



# def main():
#     print('creating db and tables')
#     create_db_and_tables()
#     print('creating users')
#     UserService.create_users()
#     print('selecting users')
#     UserService.select_users()


# if __name__ == "__main__":
#     main()