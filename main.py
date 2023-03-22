from db.models import User, Loan
from db.database import engine, create_db_and_tables
from sqlmodel import Field, Session, SQLModel, create_engine, select
import services.users as UserService
import services.loans as LoanService
from fastapi import FastAPI
from typing import List

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/users", response_model=List[User])
def get_all_users():
    return UserService.get_all_users()

@app.post("/users", response_model=User)
def create_user(user: User):
    UserService.create_user(user)
    return user

@app.get("/loans", response_model=List[Loan])
def get_all_loans():
    return LoanService.get_all_loans()

@app.post("/loans", response_model=Loan)
def create_loan(loan: Loan):
    LoanService.create_loan(loan)
    return loan



# def main():
#     print('creating db and tables')
#     create_db_and_tables()
#     print('creating users')
#     UserService.create_users()
#     print('selecting users')
#     UserService.select_users()


# if __name__ == "__main__":
#     main()