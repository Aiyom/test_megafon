from datetime import datetime

from pydantic import BaseModel


class BaseSchemas(BaseModel):
    id: str | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None


class RateAndServiceSchemas(BaseSchemas):
    name: str
    price: float
    is_rate: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserSchemas(BaseSchemas):
    name: str
    surname_name: str
    patronymic: str
    balance: float
    phone_number: str
    msisdn: int
    rate_id: RateAndServiceSchemas

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserAndCommunicationServiceSchemas(BaseSchemas):
    user_id: UserSchemas
    communication_service_id: list[RateAndServiceSchemas]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True