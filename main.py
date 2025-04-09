from fastapi import FastAPI
from app.api import members, savings, loans, transactions
from app.database import engine, Base

app = FastAPI(title="BOONA BAGAGAWALE SACCO",
              description="SACCO Management System",
              version="1.0.0")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(members.router)
app.include_router(savings.router)
app.include_router(loans.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to BOONA BAGAGAWALE SACCO"}
