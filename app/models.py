from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from .database import Base

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    member_number = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    id_number = Column(String, unique=True)
    phone = Column(String)
    email = Column(String, unique=True)
    join_date = Column(Date)
    status = Column(String)  # active/inactive

class SavingsAccount(Base):
    __tablename__ = "savings_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    account_number = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    last_updated = Column(Date)

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    loan_number = Column(String, unique=True, index=True)
    amount = Column(Float)
    interest_rate = Column(Float)
    period_months = Column(Integer)
    status = Column(String)  # pending/approved/rejected/paid
    application_date = Column(Date)
    approval_date = Column(Date, nullable=True)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    transaction_type = Column(String)  # deposit/withdrawal/loan/repayment
    amount = Column(Float)
    description = Column(String)
    date = Column(DateTime)
