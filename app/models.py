from datetime import timezone
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import INTEGER, TIMESTAMP
from database import Base

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    user_id = Column(INTEGER)

class Users(Base):
    __tablename__ = "users"

    email_address = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    user_id = Column(INTEGER)


