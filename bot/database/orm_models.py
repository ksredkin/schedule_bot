from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Integer, Column

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    grade = Column(String, nullable=False)