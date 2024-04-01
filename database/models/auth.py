from __future__ import annotations

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime

from .user import User

import datetime

session_dt = lambda: datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_as = relationship(User)
    token = Column(String, index=True, unique=True)
    valid_till = Column(DateTime, default=session_dt)

    def __repr__(self):
        return f"<Session {self.id}>"
