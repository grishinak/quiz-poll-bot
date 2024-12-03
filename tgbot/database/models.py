from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

# base class
class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), default=None, nullable=True)  ###
    question: Mapped[str] = mapped_column(String(250))
    answer: Mapped[str] = mapped_column(String(250))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Poll(Base):
    __tablename__ = "polls"

    id: Mapped[int] = mapped_column(primary_key=True)
    poll_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_collecting: Mapped[bool] = mapped_column(default=True)  # Новый флаг


class PollParticipant(Base):
    __tablename__ = "poll_participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    lobby_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    lobby_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    lobby_participant_id: Mapped[int] = mapped_column(
        ForeignKey("poll_participants.id")
    )
    answer: Mapped[str] = mapped_column(String(250))


# create all models
async def async_main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
