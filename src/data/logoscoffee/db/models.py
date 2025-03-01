from decimal import Decimal
from datetime import datetime
from typing import Any

from sqlalchemy import BIGINT, JSON, DECIMAL, ForeignKey, VARCHAR, DateTime, INT, TEXT, BOOLEAN
from sqlalchemy.orm import declarative_base, Mapped, relationship, validates
from sqlalchemy.orm import mapped_column

Base = declarative_base()

CASCADE = "CASCADE"


class UserStateOrm(Base):
    __tablename__ = "user_state"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    bot_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    state: Mapped[str | None] = mapped_column(VARCHAR, nullable=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=False)


class EventSubscriberOrm(Base):
    __tablename__ = "event_subscriber"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    event_name: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    chat_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class MenuOrm(Base):
    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    last_date_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    text_content: Mapped[str | None] = mapped_column(TEXT, nullable=True, default=None)

    @validates('text_content')
    def validate_text_content(self, key, value):
        if not value or value.strip() == '':
            raise ValueError("{key} cannot be empty or contain only spaces.")
        return value


class AdminAccountOrm(Base):
    __tablename__ = "admin_account"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(VARCHAR(16), unique=True, nullable=False)
    date_last_announcement_distributing: Mapped[datetime | None] = mapped_column(nullable=True)


class EmployeeAccountOrm(Base):
    __tablename__ = "employee_account"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(VARCHAR(16), unique=True, nullable=False)


class ClientAccountOrm(Base):
    __tablename__ = "client_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(VARCHAR(16), unique=True, nullable=False)
    client_name: Mapped[str | None] = mapped_column(VARCHAR, nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR, unique=True, nullable=False)
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    date_last_review: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ReviewOrm(Base):
    __tablename__ = "review"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    text_content: Mapped[str] = mapped_column(TEXT, nullable=False)

    @validates('text_content')
    def validate_text_content(self, key, value):
        if not value or value.strip() == '':
            raise ValueError("{key} cannot be empty or contain only spaces.")
        return value


class AnnouncementOrm(Base):
    __tablename__ = "announcement"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    date_last_distribute: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    text_content: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    preview_photo_data: Mapped[str | None] = mapped_column(VARCHAR, nullable=True)


class OrderOrm(Base):
    __tablename__ = "client_order"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    client_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(column="client_account.id", ondelete=CASCADE),
                                           nullable=False)
    pickup_code: Mapped[str | None] = mapped_column(VARCHAR(6), nullable=True)
    date_pending: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_cooking: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_ready: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_completed: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_canceled: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    cancel_details: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    details: Mapped[str | None] = mapped_column(TEXT, nullable=True)
