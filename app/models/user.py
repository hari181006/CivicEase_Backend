import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    email = Column(
        String(255),
        unique=True,
        nullable=True
    )

    phone = Column(
        String(20),
        unique=True,
        nullable=True
    )

    password_hash = Column(
        String,
        nullable=True
    )

    role = Column(
        String(30),
        default="user",
        nullable=False
    )

    # New users must complete ₹10 payment before login
    is_active = Column(
        Boolean,
        default=False,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    preferred_language = Column(
        String(10),
        default="en"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    payment_txnid = Column(
    String(100),
    nullable=True
)

payment_status = Column(
    String(30),
    default="pending",
    nullable=False
)
