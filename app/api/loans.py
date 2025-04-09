from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/", response_model=schemas.Loan)
def apply_for_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    # Check if member exists
    member = crud.get_member(db, member_id=loan.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Check if loan number exists
    db_loan = crud.get_loan_by_number(db, loan_number=loan.loan_number)
    if db_loan:
        raise HTTPException(status_code=400, detail="Loan number already exists")
    
    return crud.apply_for_loan(db=db, loan=loan)

@router.get("/", response_model=List[schemas.Loan])
def read_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    loans = crud.get_loans(db, skip=skip, limit=limit)
    return loans

@router.get("/{loan_id}", response_model=schemas.Loan)
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    db_loan = crud.get_loan(db, loan_id=loan_id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

@router.put("/{loan_id}/approve")
def approve_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = crud.approve_loan(db, loan_id=loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"message": "Loan approved", "loan_id": loan.id}

@router.post("/{loan_id}/repay")
def repay_loan(loan_id: int, amount: float, db: Session = Depends(get_db)):
    loan = crud.repay_loan(db, loan_id=loan_id, amount=amount)
    if loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return {"message": "Payment received", "loan_id": loan.id}
