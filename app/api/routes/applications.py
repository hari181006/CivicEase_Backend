import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.application import Application

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/")
def create_application(user_id: str, service_id: str, db: Session = Depends(get_db)):
    application = Application(
        user_id=user_id,
        service_id=service_id,
        application_number="CE-" + uuid.uuid4().hex[:10].upper(),
        status="submitted"
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

@router.get("/user/{user_id}")
def get_user_applications(user_id: str, db: Session = Depends(get_db)):
    return db.query(Application).filter(Application.user_id == user_id).all()
