import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum as SQLEnum,
    ForeignKey,
    Text,
    DateTime,
)
from sqlalchemy.sql import func
from src.models.base import Base


class Shelter(Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(512), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    shelter_id = Column(Integer, ForeignKey("shelters.id"), nullable=False)
    name = Column(String(100), nullable=False)
    species = Column(String(50), nullable=False)
    breed = Column(String(100))
    age = Column(Integer)
    health_status = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Role(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(Role), default=Role.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
