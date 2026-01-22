from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from email_utils import send_email
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# CORS (for Expo / frontend)
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
