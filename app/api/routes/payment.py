import os
import hashlib
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/payment", tags=["Payment"])

PAYU_KEY = os.getenv("PAYU_KEY")
PAYU_SALT = os.getenv("PAYU_SALT")

# Testing URL
PAYU_URL = "https://test.payu.in/_payment"


class PaymentRequest(BaseModel):
    email: str
    phone: str
    first_name: str


@router.post("/create")
def create_payment(data: PaymentRequest):

    if not PAYU_KEY or not PAYU_SALT:
        raise HTTPException(
            status_code=500,
            detail="PayU environment variables are missing"
        )

    txnid = "CIVIC" + uuid.uuid4().hex[:16]

    amount = "10.00"
    productinfo = "CivicEase First Registration"
    firstname = data.first_name
    email = data.email

    udf1 = ""
    udf2 = ""
    udf3 = ""
    udf4 = ""
    udf5 = ""

    hash_string = (
        f"{PAYU_KEY}|{txnid}|{amount}|{productinfo}|"
        f"{firstname}|{email}|{udf1}|{udf2}|{udf3}|{udf4}|{udf5}"
        f"|||||||||||{PAYU_SALT}"
    )

    payment_hash = hashlib.sha512(
        hash_string.encode("utf-8")
    ).hexdigest()

    return {
        "payment_url": PAYU_URL,
        "key": PAYU_KEY,
        "txnid": txnid,
        "amount": amount,
        "productinfo": productinfo,
        "firstname": firstname,
        "email": email,
        "phone": data.phone,
        "surl": "https://civicease-backend-tqt0.onrender.com/api/payment/success",
        "furl": "https://civicease-backend-tqt0.onrender.com/api/payment/failure",
        "hash": payment_hash
    }


@router.post("/success")
def payment_success():
    return {
        "status": "success",
        "message": "Payment successful"
    }


@router.post("/failure")
def payment_failure():
    return {
        "status": "failed",
        "message": "Payment failed"
    }
