from __future__ import annotations

from typing import List

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, backref

from sqlalchemy import ForeignKey, Integer, String, DateTime, Column
from sqlalchemy_utils import URLType

from sqlalchemy.orm import validates

import datetime, re
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

Base = declarative_base()
session_dt = lambda: datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    role = Column(String, index=True)
    valid_till = Column(DateTime, default=datetime.datetime.utcnow)
    guests_id = Column(Integer, ForeignKey("guest.id", ondelete='CASCADE'), nullable=True)
    users_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'), nullable=True)
    def __repr__(self):
        return f"<Organization {self.name}, role: {self.role}, validity: {self.valid_till}>"


class Guest(Base):
    __tablename__ = "guest"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    alt_email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, index=True, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    organizations: Mapped[List["Organization"]] = relationship("Organization",backref=backref("guest", passive_deletes=True), lazy='subquery')

    @validates("email", "alt_email")
    def validate_email(self, key, address):
        pat = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if re.match(pat, address):
            return address
        raise ValueError("Failed simple email validation")

    @validates("phone")
    def validate_phone(self, key, address):
        try:
            if carrier._is_mobile(number_type(phonenumbers.parse(address))):
                return address
            raise ValueError("Not a mobile number")
        except Exception:
            raise ValueError("Failed simple phone no validation")

    def __repr__(self):
        return f"<Guest {self.name}>"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    alt_email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, index=True, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    invite_id = Column(Integer, index=True, unique=True, nullable=True)
    password = Column(String)
    organizations: Mapped[List["Organization"]] = relationship("Organization", backref=backref("user", passive_deletes=True), lazy='subquery')
    sessions = relationship("SessionUser", backref=backref("user", passive_deletes=True), lazy='subquery')
    profile_photo = Column(URLType, nullable=True)

    @validates("email", "alt_email")
    def validate_email(self, key, address):
        pat = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if re.match(pat, address):
            return address
        raise ValueError("Failed simple email validation")

    @validates("phone")
    def validate_phone(self, key, address):
        try:
            if carrier._is_mobile(number_type(phonenumbers.parse(address))):
                return address
            raise ValueError("Not a mobile number")
        except Exception:
            raise ValueError("Failed simple phone no validation")

    def __repr__(self):
        return f"<User {self.name}>"

class SessionUser(Base):
    __tablename__ = "sessionsusers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    users_as = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'), nullable=True)
    token = Column(String, index=True, unique=True)
    valid_till = Column(DateTime, default=session_dt)

    def __repr__(self):
        return f"<Session {self.id}>"