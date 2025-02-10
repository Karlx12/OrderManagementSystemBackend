from datetime import datetime
from sqlalchemy import String, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Client(Base):
    __tablename__ = "Client"

    dni: Mapped[str] = mapped_column(String(8), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(9))
    balance: Mapped[float] = mapped_column(Numeric(15, 2), default=0)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(datetime.timezone.utc)
    )
