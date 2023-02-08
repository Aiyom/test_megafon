
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.database import get_session
from rate.crud import *
from rate.schemas import RateSchemas
from rate.validator import validate_price

router = APIRouter()


@router.get('/services_by_id/', status_code=status.HTTP_200_OK)
async def get_rate_by_id(service_id: str, db: AsyncSession = Depends(get_session)) -> dict:
    """
    :param service_id: получаем id тарифа для поиск
    :param db: получаем сессию для обращение к данным в бд
    :return: в результате отправим то что нашли по id  или пустой список в словарь
    """
    service = await get_rates_by_id(db, rate_id=service_id, is_rate=False)
    return {"service": service}


@router.get('/services_by_name/', status_code=status.HTTP_200_OK)
async def get_rate_by_name(name: str, db: AsyncSession = Depends(get_session)) -> dict:
    """
    :param name: Получаем имя тарифа или опцию
    :param db: получаем сессию для обращение к данным в бд
    :return: в результате отправим то что нашли по название  или пустой список в словарь
    """
    service = await get_rates_by_name(db, name=name, is_rate=False)
    return {"service": service}


@router.get('/service', status_code=status.HTTP_200_OK)
async def get_rates(db: AsyncSession = Depends(get_session), limit: int = 10, page: int = 1, search: str = '') -> dict:
    """
    :param db: получаем сессию для обращение к данным в бд
    :param limit: количество тарифов хотим получить по умолчанию 10
    :param page: количество отступов по страници по умолчанию 1
    :param search: поиск по назапнию и получить все по умолчанию пусто
    :return: возвращаем по резултиту поиска и пагинации или пустой список в словарь
    """
    skip = (page - 1) * limit
    rates, count = await get_all_rates(db, search, limit, skip, is_rate=False)
    return {'count': count, "rates": rates}


@router.post('/service', status_code=status.HTTP_201_CREATED)
async def create_new_rate(service: RateSchemas, db: AsyncSession = Depends(get_session)) -> dict:
    """
    :param service: полчаем данные для сохранение по схемы RateSchemas
    :param db: получаем сессию для обращение к данным в бд
    :return: в результате сохраним данные и возвращаем то что получили из rate
    """
    db_service = await get_rates_by_name(db, name=service.name, is_rate=False)
    price_true = await validate_price(service.price)
    if db_service or not price_true:
        raise HTTPException(status_code=400, detail="Service already exist or price must not be less than or equal to 0")
    new_service = await create_rate(db, service, False)
    return {"status": "success", "service": new_service}


@router.patch('/service', status_code=status.HTTP_200_OK)
async def update(service: RateSchemas, db: AsyncSession = Depends(get_session)) -> dict:
    """
    :param rate: полчаем данные для сохранение по схемы RateSchemas
    :param db: получаем сессию для обращение к данным в бд
    :return: в результате изменим данные и возвращаем то что получили из rate
    """
    db_rate = await get_rates_by_id(db, rate_id=service.id, is_rate=False)
    price_true = await validate_price(service.price)
    print(db_rate)
    if not db_rate or not price_true:
        raise HTTPException(status_code=400, detail=f"{service.name} is not exist or price"
                                                    f" must not be less than or equal to 0")
    await update_rate(db, service, False)
    return {"status": "success", "rate": service}
