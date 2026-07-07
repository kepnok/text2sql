from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    salary = Column(Numeric(10, 2))
    department = Column(String, index=True)
    manager = Column(String)
