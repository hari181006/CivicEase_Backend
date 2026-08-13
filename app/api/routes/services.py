from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.service import Service

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("/")
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).filter(Service.is_active == True).all()

@router.get("/{service_id}")
def get_service(service_id: str, db: Session = Depends(get_db)):
    return db.query(Service).filter(Service.id == service_id).first()
