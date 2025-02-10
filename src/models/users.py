from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .enums import UserRole


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_dni: Mapped[str] = mapped_column(String(8))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(
        type_=String, default=UserRole.EMPLOYEE
    )

    # Security fields
    failed_attempts: Mapped[int] = mapped_column(Integer, default=0)
    blocked_until: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    last_activity: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    # Audit fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(datetime.timezone.utc),
        onupdate=datetime.now(datetime.timezone.utc),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class RefreshToken(Base):
    __tablename__ = "RefreshToken"

    token_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    token_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(datetime.timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    device: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
