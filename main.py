from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from email_utils import send_email
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="FastAPI Email Service")

# CORS (for frontend / Expo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    message: str


@app.get("/")
def root():
    return {"status": "FastAPI Email Service Running"}


@app.post("/send-email")
def send_email_api(data: EmailRequest):
    try:
        send_email(
            to_email=data.to,
            subject=data.subject,
            body=data.message
        )
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/debug-env")
def debug_env():
    return {
        "SMTP_HOST": os.getenv("SMTP_HOST"),
        "SMTP_USER": os.getenv("SMTP_USER"),
        "SMTP_PASS": bool(os.getenv("SMTP_PASS")),
        "FROM_EMAIL": os.getenv("FROM_EMAIL")
    }
