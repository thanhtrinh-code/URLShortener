from sqlalchemy import Column, Integer, String, DateTime, text
from database import Base

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    clicks = Column(Integer, nullable=False)

