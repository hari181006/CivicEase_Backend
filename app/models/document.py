import uuid
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), nullable=True)
    document_type = Column(String(100), nullable=False)
    original_filename = Column(String(255))
    storage_path = Column(Text)
    mime_type = Column(String(100))
    file_size = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
