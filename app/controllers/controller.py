from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.hello import Hello, HelloRequest, HelloResponse, SessionLocal, engine, Base

router = APIRouter()

# Create DB tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create
@router.post("/hello", response_model=HelloResponse)
def create_hello(request: HelloRequest, db: Session = Depends(get_db)):
    name = request.name if request.name else "World"
    message = f"Hello, {name}!"
    db_hello = Hello(name=name, message=message)
    db.add(db_hello)
    db.commit()
    db.refresh(db_hello)
    return db_hello

# Read all
@router.get("/hello", response_model=list[HelloResponse])
def read_hellos(db: Session = Depends(get_db)):
    hellos = db.query(Hello).all()
    return hellos

# Read one
@router.get("/hello/{hello_id}", response_model=HelloResponse)
def read_hello(hello_id: int, db: Session = Depends(get_db)):
    hello = db.query(Hello).filter(Hello.id == hello_id).first()
    if not hello:
        raise HTTPException(status_code=404, detail="Hello not found")
    return hello

# Update
@router.put("/hello/{hello_id}", response_model=HelloResponse)
def update_hello(hello_id: int, request: HelloRequest, db: Session = Depends(get_db)):
    hello = db.query(Hello).filter(Hello.id == hello_id).first()
    if not hello:
        raise HTTPException(status_code=404, detail="Hello not found")
    hello.name = request.name if request.name else hello.name
    hello.message = f"Hello, {hello.name}!"
    db.commit()
    db.refresh(hello)
    return hello

# Delete
@router.delete("/hello/{hello_id}")
def delete_hello(hello_id: int, db: Session = Depends(get_db)):
    hello = db.query(Hello).filter(Hello.id == hello_id).first()
    if not hello:
        raise HTTPException(status_code=404, detail="Hello not found")
    db.delete(hello)
    db.commit()
    return {"detail": "Hello deleted"}
