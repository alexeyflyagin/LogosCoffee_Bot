from sqlalchemy import BIGINT, JSON
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
