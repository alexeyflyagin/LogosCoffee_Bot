from datetime import datetime

from sqlalchemy import BIGINT, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import declarative_base, Mapped, relationship
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

class EventSubscriberOrm(Base):
    __tablename__ = "event_subscriber"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_name: Mapped[str] = mapped_column()
    date_create: Mapped[datetime] = mapped_column(default=datetime.now)
    chat_id: Mapped[int] = mapped_column(BIGINT)


class AdminAccountOrm(Base):
    __tablename__ = "admin_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(unique=True)
    date_authorized: Mapped[datetime] = mapped_column(nullable=True)
    date_last_offer_distributing: Mapped[datetime] = mapped_column(nullable=True)

class EmployeeAccountOrm(Base):
    __tablename__ = "employee_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(unique=True)
    date_authorized: Mapped[datetime] = mapped_column(nullable=True)

class ClientAccountOrm(Base):
    __tablename__ = "client_account"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_name: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(unique=True)
    date_create: Mapped[datetime] = mapped_column(default=datetime.now)
    loyalty_points: Mapped[int] = mapped_column(default=0)
    date_last_review: Mapped[datetime] = mapped_column(nullable=True)

class ReviewOrm(Base):
    __tablename__ = "review"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(default=datetime.now)
    text_content: Mapped[str] = mapped_column()

class PromotionalOfferOrm(Base):
    __tablename__ = "promotional_offer"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(default=datetime.now)
    date_last_distribute: Mapped[datetime] = mapped_column(nullable=True)
    text_content: Mapped[str] = mapped_column(nullable=True)
    preview_photo: Mapped[str] = mapped_column(nullable=True)
