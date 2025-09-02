"""Persistence audit helpers for sessions, messages, feedback, metrics, themes."""
import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.persistence.db import AsyncSessionLocal, Session, Message, Feedback, Metric
from loguru import logger

async def record_session_start(user_id: str, name: str) -> int:
    """Create a new session and return its ID."""
    async with AsyncSessionLocal() as db:
        s = Session(user_id=user_id, name=name)
        db.add(s)
        await db.commit()
        await db.refresh(s)
        logger.info(f"Session started: {s.id}")
        return s.id

async def record_session_end(session_id: int) -> None:
    """Mark session as ended (no-op, for future extension)."""
    logger.info(f"Session ended: {session_id}")

async def record_session_name(session_id: int, name: str) -> None:
    """Rename a session."""
    async with AsyncSessionLocal() as db:
        await db.execute(update(Session).where(Session.id == session_id).values(name=name))
        await db.commit()
        logger.info(f"Session renamed: {session_id} -> {name}")

async def get_sessions(user_id: str) -> List[Dict[str, Any]]:
    """Get all sessions for a user."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Session).where(Session.user_id == user_id))
        return [s.__dict__ for s in result.scalars().all()]

async def record_message(session_id: int, role: str, content: str) -> int:
    """Record a message and return its ID."""
    async with AsyncSessionLocal() as db:
        m = Message(session_id=session_id, role=role, content=content)
        db.add(m)
        await db.commit()
        await db.refresh(m)
        logger.info(f"Message recorded: {m.id}")
        return m.id

async def get_session_messages(session_id: int) -> List[Dict[str, Any]]:
    """Get all messages for a session."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Message).where(Message.session_id == session_id))
        return [m.__dict__ for m in result.scalars().all()]

async def record_message_feedback(session_id: int, message_id: int, rating: int, comment: Optional[str] = None) -> int:
    """Record feedback for a message."""
    async with AsyncSessionLocal() as db:
        f = Feedback(session_id=session_id, message_id=message_id, rating=rating, comment=comment)
        db.add(f)
        await db.commit()
        await db.refresh(f)
        logger.info(f"Message feedback recorded: {f.id}")
        return f.id

async def record_session_feedback(session_id: int, rating: int, comment: Optional[str] = None) -> int:
    """Record feedback for a session."""
    async with AsyncSessionLocal() as db:
        f = Feedback(session_id=session_id, message_id=None, rating=rating, comment=comment)
        db.add(f)
        await db.commit()
        await db.refresh(f)
        logger.info(f"Session feedback recorded: {f.id}")
        return f.id

async def record_metrics(session_id: int, key: str, value: str) -> int:
    """Record a metric for a session."""
    async with AsyncSessionLocal() as db:
        m = Metric(session_id=session_id, key=key, value=value)
        db.add(m)
        await db.commit()
        await db.refresh(m)
        logger.info(f"Metric recorded: {m.id}")
        return m.id

async def record_session_theme(session_id: int, theme: str) -> None:
    """Persist theme for a session."""
    async with AsyncSessionLocal() as db:
        await db.execute(update(Session).where(Session.id == session_id).values(theme=theme))
        await db.commit()
        logger.info(f"Session theme updated: {session_id} -> {theme}")

async def get_session_theme(session_id: int) -> Optional[str]:
    """Get theme for a session."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Session.theme).where(Session.id == session_id))
        theme = result.scalar_one_or_none()
        logger.info(f"Session theme fetched: {session_id} -> {theme}")
        return theme

async def delete_session_data(session_id: int) -> None:
    """Delete all data for a session."""
    async with AsyncSessionLocal() as db:
        await db.execute(delete(Message).where(Message.session_id == session_id))
        await db.execute(delete(Feedback).where(Feedback.session_id == session_id))
        await db.execute(delete(Metric).where(Metric.session_id == session_id))
        await db.execute(delete(Session).where(Session.id == session_id))
        await db.commit()
        logger.info(f"Session deleted: {session_id}")
