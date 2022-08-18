from sqlalchemy import Column, String

from .base import Base


__all__ = [
    'Employe'
]


class Employe(Base):
    __tablename__ = 'employees'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    role = Column(String)
    password = Column(String)
