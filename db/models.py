from typing import Optional
from sqlmodel import Field, SQLModel

class Loan(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    apr: float = Field()
    term: int = Field()
    principle: int = Field()
    monthly_payment: float = Field()


class User(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    first: str = Field()
    last: str = Field()

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

