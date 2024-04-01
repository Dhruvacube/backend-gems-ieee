from __future__ import annotations

from typing import List

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates

import datetime, re
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

Base = declarative_base()


class Organization(Base):
    __tablename__ = "organizations"

    id = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = mapped_column(String, index=True)
    role = mapped_column(String, index=True)
    valid_till = mapped_column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Organization {self.name}, role: {self.role}, validity: {self.valid_till}>"


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    alt_email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, index=True, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    organizations: Mapped[List["Organization"]] = relationship(back_populates="guests")

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
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    alt_email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, index=True, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
    invite_id = Column(String, index=True, unique=True, nullable=True)
    hashed_password = Column(String)
    organizations: Mapped[List["Organization"]] = relationship(back_populates="users")
    profile_photo = Column(String, nullable=True)

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
        return f"<User {self.username}>"
