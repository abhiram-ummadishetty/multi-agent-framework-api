from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import get_settings
from db.models import Base, ChatThread, ChatMessage, Feedback

settings = get_settings()

database_url = settings.database_url

engine = create_async_engine(database_url, echo=settings.db_echo_sql, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


async def seed_db():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ChatThread).limit(1))
        if result.scalars().first() is not None:
            return

        sample_thread = ChatThread(
            session_id="seed-session-001",
            user_id="seed-user",
        )

        sample_messages = [
            ChatMessage(
                thread=sample_thread,
                role="user",
                content="Hello! Can you summarize the latest product roadmap?",
            ),
            ChatMessage(
                thread=sample_thread,
                role="assistant",
                content="Sure. The roadmap focuses on improved agent orchestration, better error handling, and PostgreSQL persistence for chat history.",
            ),
        ]

        sample_feedback = Feedback(
            feedback_id="seed-feedback-001",
            session_id=sample_thread.session_id,
            message_id=None,
            rating=5,
            comment="The response was helpful and well-structured.",
        )

        session.add(sample_thread)
        session.add_all(sample_messages)
        session.add(sample_feedback)
        await session.commit()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_db()
