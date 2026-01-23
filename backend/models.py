from sqlalchemy import Column, String, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.sql import func
from database import Base
from uuid import uuid4

from pydantic import BaseModel

class MailboxCreate(BaseModel):
    name: str
    target_url: str


class Mailbox(Base):
    __tablename__ = "mailboxes"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String)
    api_key = Column(String)
    target_url = Column(String)
    created_at = Column(DateTime, server_default=func.now())


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    tracking_number = Column(String, primary_key=True, default=lambda: str(uuid4()))
    mailbox_id = Column(String, ForeignKey("mailboxes.id"))
    payload = Column(JSON)
    status = Column(String, default="pending")
    created_at = Column(DateTime, server_default=func.now())


class WebhookAttempt(Base):
    __tablename__ = "webhook_attempts"

    id = Column(Integer, primary_key=True)
    tracking_number = Column(String)
    attempt_number = Column(Integer)
    status = Column(String)
    error = Column(String, nullable=True)
    attempted_at = Column(DateTime, server_default=func.now())
