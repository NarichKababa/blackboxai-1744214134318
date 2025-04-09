from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import schemas, crud, models
from ..database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    # Verify member exists
    member = crud.get_member(db, member_id=transaction.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Create transaction record
    db_transaction = models.Transaction(
        member_id=transaction.member_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        description=transaction.description,
        date=datetime.now()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions

@router.get("/member/{member_id}", response_model=List[schemas.Transaction])
def read_member_transactions(member_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    member = crud.get_member(db, member_id=member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    transactions = db.query(models.Transaction)\
        .filter(models.Transaction.member_id == member_id)\
        .offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction)\
        .filter(models.Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
