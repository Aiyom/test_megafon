
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.database import get_session
from rate.crud import get_all_rates, get_rates_by_id, create_rate, get_rates_by_name, update_rate
from rate.schemas import RateSchemas
from rate.validator import validate_price

router = APIRouter()


@router.get('/rate_by_id/', status_code=status.HTTP_200_OK)
async def get_rate_by_id(rate_id: str, db: AsyncSession = Depends(get_session)) -> dict:
    """
    :param rate_id: получаем id тарифа для поиск
    :param db: получаем сессию для обращение к данным в бд
    :return: в результате отправим то что нашли по id  или пустой список в словарь
    """
    rate = await get_rates_by_id(db, rate_id=rate_id)
    return {"rates": rate}


@router.get('/rate_by_name/', status_code=status.HTTP_200_OK)
async def get_rate_by_name(name: str, db: AsyncSession = Depends(get_session)) -> dict:
    """
    :param name: Получаем имя тарифа или опцию
    :param db: получаем сессию для обращение к данным в бд
    :return: в результате отправим то что нашли по название  или пустой список в словарь
    """
    rate = await get_rates_by_name(db, name=name)
    return {"rates": rate}


@router.get('/rate', status_code=status.HTTP_200_OK)
async def get_rates(db: AsyncSession = Depends(get_session), limit: int = 10, page: int = 1, search: str = '') -> dict:
    """
    :param db: получаем сессию для обращение к данным в бд
    :param limit: количество тарифов хотим получить по умолчанию 10
    :param page: количество отступов по страници по умолчанию 1
    :param search: поиск по назапнию и получить все по умолчанию пусто
    :return: возвращаем по резултиту поиска и пагинации или пустой список в словарь
    """
    skip = (page - 1) * limit
    rates, count = await get_all_rates(db, search, limit, skip)
    return {'count': count, "rates": rates}


@router.post('/rate', status_code=status.HTTP_201_CREATED)
async def create_new_rate(rate: RateSchemas, db: AsyncSession = Depends(get_session)) -> dict:
    """
    :param rate: полчаем данные для сохранение по схемы RateSchemas
    :param db: получаем сессию для обращение к данным в бд
    :return: в результате сохраним данные и возвращаем то что получили из rate
    """
    db_rate = await get_rates_by_name(db, name=rate.name)
    price_true = await validate_price(rate.price)
    if db_rate or not price_true:
        raise HTTPException(status_code=400, detail="Rate already exist or price must not be less than or equal to 0")
    new_rate = await create_rate(db, rate)
    return {"status": "success", "rates": new_rate}


@router.patch('/rate', status_code=status.HTTP_200_OK)
async def update(rate: RateSchemas, db: AsyncSession = Depends(get_session)) -> dict:
    """
    :param rate: полчаем данные для сохранение по схемы RateSchemas
    :param db: получаем сессию для обращение к данным в бд
    :return: в результате изменим данные и возвращаем то что получили из rate
    """
    db_rate = await get_rates_by_id(db, rate_id=rate.id)
    price_true = await validate_price(rate.price)
    if not db_rate or not price_true:
        raise HTTPException(status_code=400, detail=f"{rate.name} is not exist or price"
                                                    f" must not be less than or equal to 0")
    await update_rate(db, rate)
    return {"status": "success", "rate": rate}
