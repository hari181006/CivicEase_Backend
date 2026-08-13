import uuid
from sqlalchemy import Boolean, Column, DateTime, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class Service(Base):
    __tablename__ = "services"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    category = Column(String(100))
    description = Column(Text)
    official_authority = Column(String(255))
    official_url = Column(Text)
    application_url = Column(Text)
    service_type = Column(String(30), default="official")
    government_fee = Column(Numeric(12, 2), default=0)
    service_fee = Column(Numeric(12, 2), default=0)
    processing_information = Column(Text)
    is_active = Column(Boolean, default=True)
    last_verified_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
