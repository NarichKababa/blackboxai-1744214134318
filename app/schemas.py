from datetime import date
from pydantic import BaseModel, EmailStr

class MemberBase(BaseModel):
    member_number: str
    first_name: str
    last_name: str
    id_number: str
    phone: str
    email: EmailStr

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: int
    join_date: date
    status: str

    class Config:
        from_attributes = True

class SavingsAccountBase(BaseModel):
    member_id: int
    account_number: str

class SavingsAccountCreate(SavingsAccountBase):
    pass

class SavingsAccount(SavingsAccountBase):
    id: int
    balance: float
    last_updated: date

    class Config:
        from_attributes = True

class LoanBase(BaseModel):
    member_id: int
    loan_number: str
    amount: float
    interest_rate: float
    period_months: int

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    status: str
    application_date: date
    approval_date: date | None

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    member_id: int
    transaction_type: str
    amount: float
    description: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True
