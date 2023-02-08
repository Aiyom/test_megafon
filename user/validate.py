from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from rate.crud import get_rates_by_id
from user.crud import get_user_by_phone_number
from user.schemas import UserSchemas


async def check_balance_when_edit_rate_or_service(db: AsyncSession, user: UserSchemas, is_rate: bool = True) -> bool:
    """
    Тут проверяем если у юзера изменился тариф тогда проверим баланс если не изменилось то пропускаем
    :param db: Получаем сессию для бд
    :param user: получаем данные о юзере с схемой UserSchemas
    :return: если тариф меняли и баланс больше чем цена тарифа возращаем True или если тариф не меняли тоже True 
    в других случаях даем ошибку что баланс не достатично
    """
    rate_and_service = await get_rates_by_id(db, user.rate_id.id, is_rate)
    user_on_db = await get_user_by_phone_number(db, user.phone_number)
    if user.rate_id.id != str(user_on_db[0].rate_id) and user.balance > rate_and_service[0].price:
        return True
    elif user.rate_id.id == str(user_on_db[0].rate_id):
        return True
    raise HTTPException(status_code=400, detail=f"{user.name} not enough balance")
