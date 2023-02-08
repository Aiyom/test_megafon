import uuid

from sqlalchemy import Column, String, Float, BigInteger, ForeignKey, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base


class BaseTable(Base):

    __abstract__ = True

    # id = Column(GUID, primary_key=True, default=uuid.uuid4)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(BaseTable):
    __tablename__ = 'users'

    name = Column(String)
    surname_name = Column(String)
    patronymic = Column(String, nullable=True)
    balance = Column(Float)
    phone_number = Column(String)
    msisdn = Column(BigInteger)
    rate_id = Column(UUID(as_uuid=True), ForeignKey("rates_and_services.id"), nullable=False)


class RateAndService(BaseTable):

    __tablename__ = 'rates_and_services'

    name = Column(String)
    price = Column(Float)
    user_id = relationship("User")
    is_rate = Column(Boolean, default=False)


class UserAndCommunicationService(BaseTable):
    __tablename__ = 'user_and_communication_service'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    communication_service_id = Column(UUID(as_uuid=True), ForeignKey("rates_and_services.id"))