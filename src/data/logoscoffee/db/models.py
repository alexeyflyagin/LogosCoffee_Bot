from datetime import datetime

from sqlalchemy import BIGINT, JSON, DateTime
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.orm import mapped_column


Base = declarative_base()


class UserStateOrm(Base):
    __tablename__ = "user_state"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bot_id: Mapped[int] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(BIGINT)
    chat_id: Mapped[int] = mapped_column(BIGINT)
    state: Mapped[str] = mapped_column(nullable=True)
    data: Mapped[dict] = mapped_column(JSON)

class AdminAccountOrm(Base):
    __tablename__ = "admin_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(VARCHAR(8), unique=True)

class EmployeeAccountOrm(Base):
    __tablename__ = "employee_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(VARCHAR(8), unique=True)

class ClientAccountOrm(Base):
    __tablename__ = "client_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(VARCHAR(8), unique=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR, unique=True)
    date_registration: Mapped[datetime] = mapped_column()
    loyalty_points: Mapped[int] = mapped_column(default=0)
    date_last_review: Mapped[datetime] = mapped_column(nullable=True)

class ReviewOrm(Base):
    __tablename__ = "review"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column()
    text_content: Mapped[str] = mapped_column(VARCHAR)