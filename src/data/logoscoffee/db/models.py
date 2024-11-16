from decimal import Decimal
from datetime import datetime
from typing import Any

from sqlalchemy import BIGINT, JSON, DECIMAL, ForeignKey, VARCHAR
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.orm import mapped_column


Base = declarative_base()

CASCADE = "CASCADE"


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
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)


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

class ProductOrm(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(default=datetime.now)
    is_available: Mapped[bool] = mapped_column(default=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL)
    product_name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    preview_photo: Mapped[str] = mapped_column(nullable=True)

class ProductAndOrderOrm(Base):
    __tablename__ = "product_and_order"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(default=datetime.now)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id", ondelete=CASCADE))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete=CASCADE))

class OrderOrm(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_create: Mapped[datetime] = mapped_column(default=datetime.now)
    client_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(column="client_account.id", ondelete=CASCADE))
    pickup_code: Mapped[str] = mapped_column(VARCHAR(4), nullable=True)
    date_pending: Mapped[datetime] = mapped_column(default=datetime.now, nullable=True)
    date_cooking: Mapped[datetime] = mapped_column(default=datetime.now, nullable=True)
    date_ready: Mapped[datetime] = mapped_column(default=datetime.now, nullable=True)
    date_completed: Mapped[datetime] = mapped_column(default=datetime.now, nullable=True)
    date_canceled: Mapped[datetime] = mapped_column(default=datetime.now, nullable=True)
    cancel_details: Mapped[str] = mapped_column(nullable=True)
    details: Mapped[str] = mapped_column(nullable=True)



