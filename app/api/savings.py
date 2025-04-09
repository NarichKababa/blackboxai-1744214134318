from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/savings", tags=["savings"])

@router.post("/accounts/", response_model=schemas.SavingsAccount)
def create_account(account: schemas.SavingsAccountCreate, db: Session = Depends(get_db)):
    db_account = crud.get_account_by_number(db, account_number=account.account_number)
    if db_account:
        raise HTTPException(status_code=400, detail="Account number already exists")
    return crud.create_savings_account(db=db, account=account)

@router.get("/accounts/", response_model=List[schemas.SavingsAccount])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = crud.get_savings_accounts(db, skip=skip, limit=limit)
    return accounts

@router.get("/accounts/{account_id}", response_model=schemas.SavingsAccount)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_savings_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.post("/accounts/{account_id}/deposit")
def deposit(account_id: int, amount: float, db: Session = Depends(get_db)):
    account = crud.deposit_to_account(db, account_id=account_id, amount=amount)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Deposit successful", "new_balance": account.balance}

@router.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: int, amount: float, db: Session = Depends(get_db)):
    account = crud.withdraw_from_account(db, account_id=account_id, amount=amount)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Withdrawal successful", "new_balance": account.balance}
