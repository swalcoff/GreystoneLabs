from typing import Optional
from sqlmodel import Field, SQLModel

class Loan(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    apr: float = Field()
    term: int = Field()

class User(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    first: str = Field()
    last: str = Field()

class User_Loan(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key=True, nullable=False)
    userid: int = Field()
    loanid: int = Field()
