from sqlalchemy import Column, String, DateTime

from .base import Base


__all__ = [
    'AuthToken',
    'RefreshToken'
]


class AuthToken(Base):
    __tablename__ = 'auth_tokens'

    token = Column(String, primary_key=True)
    employee_id = Column(String)
    valid_until = Column(DateTime)

    browser = Column(String, nullable=True)
    browser_version = Column(String, nullable=True)

    os = Column(String, nullable=True)
    os_version = Column(String, nullable=True)

    device_family = Column(String, nullable=True)
    device_brand = Column(String, nullable=True)
    device_model = Column(String, nullable=True)


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    refresh_token = Column(String, primary_key=True)
    auth_token = Column(String, unique=True)
    valid_until = Column(DateTime)
