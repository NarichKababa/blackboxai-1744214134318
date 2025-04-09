from sqlalchemy.orm import Session
from . import models, schemas

def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()

def get_member_by_number(db: Session, member_number: str):
    return db.query(models.Member).filter(models.Member.member_number == member_number).first()

def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_savings_account(db: Session, account_id: int):
    return db.query(models.SavingsAccount).filter(models.SavingsAccount.id == account_id).first()

def create_savings_account(db: Session, account: schemas.SavingsAccountCreate):
    db_account = models.SavingsAccount(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def deposit_to_account(db: Session, account_id: int, amount: float):
    account = get_savings_account(db, account_id)
    if account:
        account.balance += amount
        db.commit()
        db.refresh(account)
    return account

def apply_for_loan(db: Session, loan: schemas.LoanCreate):
    db_loan = models.Loan(**loan.dict(), status="pending")
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def get_loan(db: Session, loan_id: int):
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()
