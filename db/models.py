from typing import Optional
from sqlmodel import Field, SQLModel

class Loan(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    apr: float = Field()
    term: int = Field()
    principle: int = Field()
    monthly_payment: Optional[float] = Field()

class LoanCreate(SQLModel):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    apr: float = Field()
    term: int = Field()
    principle: int = Field()
    userid: int = Field()


class User(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    name: str = Field()

class User_Loan(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    userid: int = Field()
    loanid: int = Field()

class Loan_Summary(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    loanid: int = Field()
    month: int = Field()
    balance: float = Field()
    payment: float = Field()
    principle: float = Field()
    interest: float = Field()
    total_interest: float = Field()
    total_principle: float = Field()

class Loan_Schedule_Read(SQLModel):
    month: int = Field()
    balance: float = Field()
    payment: float = Field()

class Loan_Summary_Read(SQLModel):
    balance: float = Field
    total_principle: float = Field()
    total_interest: float = Field()
