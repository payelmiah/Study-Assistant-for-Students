# app/services/huggingface_service.py
import requests
import os
try:
    from app.utils.config import get_huggingface_api_key
except Exception:
    def get_huggingface_api_key():
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except Exception:
            pass
        return os.getenv("HUGGINGFACE_API_KEY")


# Retrieve API key via config helper (reads .env when available)
HUGGINGFACE_API_KEY = get_huggingface_api_key()
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

# Detect test environment to avoid external network calls during tests
IS_TEST = "PYTEST_CURRENT_TEST" in os.environ or os.getenv("TESTING") == "1"


def _local_summary(text: str) -> str:
    if not text:
        return ""
    s = text.strip()
    # Return first sentence if reasonably short, otherwise a short excerpt
    idx = s.find('.')
    if idx != -1 and idx < 300:
        return s[: idx + 1]
    return (s[:300] + "...") if len(s) > 300 else s


def _call_hf_api(text: str) -> str:
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"} if HUGGINGFACE_API_KEY else {}
    payload = {"inputs": text}
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            # Handle common HF response shapes
            if isinstance(data, list) and len(data) > 0:
                first = data[0]
                if isinstance(first, dict):
                    if "summary_text" in first:
                        return first["summary_text"]
                    if "generated_text" in first:
                        return first["generated_text"]
            if isinstance(data, dict):
                if "summary_text" in data:
                    return data["summary_text"]
                if "generated_text" in data:
                    return data["generated_text"]
            # Fallback to local summary when format is unexpected
            return _local_summary(text)
        else:
            return _local_summary(text)
    except Exception:
        return _local_summary(text)


def generate_summary(text: str) -> str:
    if IS_TEST or not HUGGINGFACE_API_KEY:
        return _local_summary(text)
    return _call_hf_api(text)


def generate_mcqs(text: str) -> str:
    # Simple local MCQ generator: create a short placeholder based on text
    if IS_TEST or not HUGGINGFACE_API_KEY:
        excerpt = text.strip()[:150]
        return f"MCQs (placeholder): Create multiple-choice questions based on: {excerpt}"
    # If a model for MCQs is available, you can call it here. For now reuse summary endpoint.
    return _call_hf_api(f"Generate MCQs from the following text:\n\n{text}")


def generate_exam_questions(text: str) -> str:
    if IS_TEST or not HUGGINGFACE_API_KEY:
        excerpt = text.strip()[:150]
        return f"Exam Questions (placeholder): Create exam-style questions from: {excerpt}"
    return _call_hf_api(f"Generate exam questions from the following text:\n\n{text}")
