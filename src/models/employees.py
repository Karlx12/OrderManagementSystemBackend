from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .enums import UserRole, EmployeeStatus


class Employee(Base):
    __tablename__ = "Employee"

    dni: Mapped[str] = mapped_column(String(8), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(9))
    role: Mapped[UserRole] = mapped_column(type_=String)
    hire_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(datetime.timezone.utc)
    )
    status: Mapped[EmployeeStatus] = mapped_column(
        type_=String, default=EmployeeStatus.ACTIVE
    )
