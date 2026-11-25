import os
import base64
from datetime import datetime
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Warm Hearts NGO API & Web Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DARAJA_ENV = os.getenv("DARAJA_ENV", "sandbox")
BASE_URL = "https://api.safaricom.co.ke" if DARAJA_ENV == "production" else "https://sandbox.safaricom.co.ke"

CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY", "")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "")
SHORTCODE = os.getenv("MPESA_SHORTCODE", "174379")
PASSKEY = os.getenv("MPESA_PASSKEY", "")
CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL", "https://your-domain.onrender.com/api/mpesa/callback")


class StkPushRequest(BaseModel):
    phone_number: str
    amount: int
    cause: str = "Warm Hearts Donation"


async def get_daraja_token() -> str:
    if not CONSUMER_KEY or not CONSUMER_SECRET:
        raise HTTPException(status_code=503, detail="Daraja credentials not configured in environment.")
    auth_str = base64.b64encode(f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()).decode()
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(
            f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            headers={"Authorization": f"Basic {auth_str}"}
        )
        resp.raise_for_status()
        return resp.json()["access_token"]


@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")


@app.post("/api/mpesa/stkpush")
async def initiate_stk_push(payload: StkPushRequest):
    if payload.amount < 1:
        raise HTTPException(status_code=400, detail="Amount must be at least KES 1")

    token = await get_daraja_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()

    daraja_payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": payload.amount,
        "PartyA": payload.phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": payload.phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "WarmHearts",
        "TransactionDesc": payload.cause[:12] or "Donation"
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(
            f"{BASE_URL}/mpesa/stkpush/v1/processrequest",
            json=daraja_payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        return resp.json()


@app.post("/api/mpesa/callback")
async def mpesa_callback(request: Request):
    data = await request.json()
    print("M-Pesa Callback Received:", data)
    return {"ResultCode": 0, "ResultDesc": "Accepted"}
