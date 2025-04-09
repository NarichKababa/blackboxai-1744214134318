from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/members", tags=["members"])

@router.post("/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = crud.get_member_by_number(db, member_number=member.member_number)
    if db_member:
        raise HTTPException(status_code=400, detail="Member number already registered")
    return crud.create_member(db=db, member=member)

@router.get("/", response_model=List[schemas.Member])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    members = crud.get_members(db, skip=skip, limit=limit)
    return members

@router.get("/{member_id}", response_model=schemas.Member)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@router.put("/{member_id}", response_model=schemas.Member)
def update_member(member_id: int, member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud.update_member(db=db, member_id=member_id, member=member)

@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    crud.delete_member(db=db, member_id=member_id)
    return {"message": "Member deleted successfully"}
