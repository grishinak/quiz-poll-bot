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


class Poll(Base):
    __tablename__ = "polls"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    question: Mapped[str] = mapped_column(String(250))
    answer: Mapped[str] = mapped_column(String(250))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Lobby(Base):
    __tablename__ = "lobbies"

    id: Mapped[int] = mapped_column(primary_key=True)
    poll_id: Mapped[int] = mapped_column(ForeignKey("polls.id"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class LobbyParticipant(Base):
    __tablename__ = "lobby_participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    lobby_id: Mapped[int] = mapped_column(ForeignKey("lobbies.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    lobby_id: Mapped[int] = mapped_column(ForeignKey("lobbies.id"))
    lobby_participant_id: Mapped[int] = mapped_column(
        ForeignKey("lobby_participants.id")
    )
    answer: Mapped[str] = mapped_column(String(250))


# create all models
async def async_main():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
