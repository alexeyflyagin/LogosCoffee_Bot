from sqlalchemy import BIGINT, JSON
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.orm import mapped_column

Base = declarative_base()

class UserState(Base):
    __tablename__ = "user_state"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bot_id: Mapped[int] = mapped_column(BIGINT)
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    state: Mapped[str] = mapped_column(nullable=True)
    data: Mapped[dict] = mapped_column(JSON)

