# importing for .env
import os
from dotenv import load_dotenv

from sqlalchemy import BigInteger, String, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()
engine = create_async_engine(url=os.getenv("DB_URL"))

async_session = async_sessionmaker(engine)

# base class
class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    tg_id = mapped_column(BigInteger, primary_key=True)  # Add unique constraint
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(250))
    answer: Mapped[str] = mapped_column(String(250))
    creator_tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))


class Poll(Base):
    __tablename__ = "polls"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    creator_tg_id: Mapped[BigInteger] = mapped_column(ForeignKey("users.tg_id"))
    is_collecting: Mapped[bool] = mapped_column(Boolean, default=True)  # Новый флаг


class PollParticipant(Base):
    __tablename__ = "poll_participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    user_tg_id: Mapped[BigInteger] = mapped_column(ForeignKey("users.tg_id"))


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    lobby_participant_id: Mapped[BigInteger] = mapped_column(
        ForeignKey("users.tg_id")  # tg_id
    )
    answer: Mapped[str] = mapped_column(String(250))


# create all models
async def async_main():

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
