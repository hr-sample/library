from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(BaseModel):
    serial_number: int
    title: str
    author: str
    borrower: Optional[int]
    borrowed_at: Optional[datetime]
    is_taken: bool

    @field_validator("serial_number")
    def check_serial_number(cls, v: int) -> int:
        if not (100_000 <= v <= 999_999):
            raise ValueError("Invalid serial number.")
        return v

    @field_validator("borrower")
    def check_borrower(cls, v: int | None) -> int | None:
        if v is not None and not (100_000 <= v <= 999_999):
            raise ValueError("Invalid serial number.")
        return v


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    borrower: Optional[int] = None
    borrowed_at: Optional[datetime] = None
    is_taken: Optional[bool] = None

    @field_validator("borrower")
    def check_borrower(cls, v: int | None) -> int | None:
        if v is not None and not (100_000 <= v <= 999_999):
            raise ValueError("Invalid serial number.")
        return v


class DbBook(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    serial_number = Column(Integer, unique=True, index=True)
    title = Column(String(255))
    author = Column(String(255))
    borrower = Column(Integer)
    is_taken = Column(Boolean)
    borrowed_at = Column(DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
