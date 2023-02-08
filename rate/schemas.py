from datetime import datetime

from user.schemas import BaseSchemas


class RateSchemas(BaseSchemas):
    name: str
    price: float
    is_rate: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True