# app/api/document.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.huggingface_service import generate_summary, generate_mcqs, generate_exam_questions

router = APIRouter()

class Document(BaseModel):
    content: str


@router.post("/generate_summary/")
async def generate_summary_endpoint(doc: Document):
    summary = generate_summary(doc.content)
    return {"summary": summary}

@router.post("/generate_mcqs/")
async def generate_mcqs_endpoint(doc: Document):
    mcqs = generate_mcqs(doc.content)
    return {"mcqs": mcqs}

@router.post("/generate_exam_questions/")
async def generate_exam_questions_endpoint(doc: Document):
    questions = generate_exam_questions(doc.content)
    return {"exam_questions": questions}
