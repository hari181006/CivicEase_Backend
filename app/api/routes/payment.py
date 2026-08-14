import os
import hashlib
import uuid

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User


router = APIRouter(prefix="/payment", tags=["Payment"])


PAYU_KEY = os.getenv("PAYU_KEY")
PAYU_SALT = os.getenv("PAYU_SALT")

PAYU_URL = "https://test.payu.in/_payment"


class PaymentRequest(BaseModel):
    email: str
    phone: str
    first_name: str


@router.post("/create")
def create_payment(
    data: PaymentRequest,
    db: Session = Depends(get_db)
):

    if not PAYU_KEY or not PAYU_SALT:
        raise HTTPException(
            status_code=500,
            detail="PayU environment variables are missing"
        )

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
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

    # Save transaction ID
    user.payment_txnid = txnid
    user.payment_status = "pending"

    db.commit()

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
async def payment_success(
    request: Request,
    db: Session = Depends(get_db)
):

    form_data = await request.form()

    txnid = form_data.get("txnid")
    status = form_data.get("status")

    if not txnid:
        raise HTTPException(
            status_code=400,
            detail="Transaction ID missing"
        )

    user = db.query(User).filter(
        User.payment_txnid == txnid
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User transaction not found"
        )

    if status == "success":

        user.is_active = True
        user.payment_status = "paid"

        db.commit()

        return {
            "status": "success",
            "message": "₹10 payment successful. Account activated.",
            "user_id": str(user.id)
        }

    raise HTTPException(
        status_code=400,
        detail="Payment was not successful"
    )


@router.post("/failure")
async def payment_failure(
    request: Request,
    db: Session = Depends(get_db)
):

    form_data = await request.form()

    txnid = form_data.get("txnid")

    if txnid:
        user = db.query(User).filter(
            User.payment_txnid == txnid
        ).first()

        if user:
            user.payment_status = "failed"
            db.commit()

    return {
        "status": "failed",
        "message": "Payment failed. Please try again."
    }
