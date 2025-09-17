from fastapi import FastAPI
from app.controllers.controller import router

app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI application",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Hello World API!"}