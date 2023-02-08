import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as update_execute, select, func

from user import models
from . import schemas

logger = logging.getLogger(__name__)


async def get_all_rates(db: AsyncSession, search: str, limit: int, skip: int, is_rate: bool = True) -> Any:
    try:
        count_rate = await db.execute(
            select([func.count(), models.RateAndService])
            .filter(models.RateAndService.name.contains(search))
            .filter(models.RateAndService.is_rate == is_rate)
            .group_by(models.RateAndService.id)
        )
        rates = await db.execute(
            select(models.RateAndService)
            .filter(models.RateAndService.name.contains(search))
            .filter(models.RateAndService.is_rate == is_rate)
            .order_by(models.RateAndService.id)
            .limit(limit)
            .offset(skip))
        return (rates.fetchall(), sum(count_rate.scalars().all()))
    except Exception as e:
        logger.warning(str(e))


async def get_rates_by_id(db: AsyncSession, rate_id: str, is_rate: bool = True) -> schemas.RateSchemas:
    try:
        user = await db.execute(
            select(models.RateAndService)
            .filter(
                models.RateAndService.id == rate_id
            )
            .filter(models.RateAndService.is_rate == is_rate)
        )
        return user.fetchone()
    except Exception as e:
        logger.warning(str(e))


async def get_rates_by_name(db: AsyncSession, name: str = None, is_rate: bool = True) -> schemas.RateSchemas:
    try:
        user = await db.execute(
            select(models.RateAndService)
            .filter(
                models.RateAndService.name == name
            )
            .filter(models.RateAndService.is_rate == is_rate)
        )
        return user.fetchall()
    except Exception as e:
        logger.warning(str(e))


async def create_rate(db: AsyncSession, rate: schemas.RateSchemas, is_rate: bool = True) -> schemas.RateSchemas:
    try:
        rate_and_service = models.RateAndService(
            name=rate.name,
            price=rate.price,
            is_rate=is_rate if is_rate is not None else False
        )
        db.add(rate_and_service)
        await db.commit()
        return rate_and_service
    except Exception as e:
        logger.warning(str(e))


async def update_rate(db: AsyncSession, rate: schemas.RateSchemas, is_rate: bool = True):
    try:
        update = await db.execute(
            update_execute(models.RateAndService)
            .where(models.RateAndService.id == rate.id)
            .values(
                name=rate.name,
                price=rate.price,
                is_rate=is_rate
            )
            .execution_options(synchronize_session="fetch")
        )
        await db.commit()
        return update.scalar()
    except Exception as e:
        logger.warning(str(e))