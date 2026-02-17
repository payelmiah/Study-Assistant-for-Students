# app/main.py
from fastapi import FastAPI
from app.api.document import router as document_router
from app.api.health import router as health_router

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Student Assistant API!"}

# Include routers
app.include_router(document_router)
app.include_router(health_router)
