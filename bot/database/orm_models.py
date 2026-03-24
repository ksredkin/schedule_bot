from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Integer, BigInteger, Column

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    grade = Column(String, nullable=False)