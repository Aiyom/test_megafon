import logging

from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
from sqlalchemy import update as update_execute, select

from rate import schemas as rate_schemas
from rate.crud import get_rates_by_id
from user import models, schemas

logger = logging.getLogger(__name__)


async def get_all_users(db: AsyncSession, search, limit, skip):
    try:
        users = await db.execute(
            select(models.User, models.RateAndService)
            .filter(models.User.name.contains(search))
            .filter(models.User.rate_id == models.RateAndService.id)
            .limit(limit)
            .offset(skip))
        return users.fetchall()
    except Exception as e:
        logger.warning(str(e))


async def get_user_by_phone_number(db: AsyncSession, phone_number: str):
    try:
        user = await db.execute(
            select(models.User, models.RateAndService)
            .filter(models.User.rate_id == models.RateAndService.id)
            .where(
                models.User.phone_number.contains(phone_number)
            ))
        return user.fetchone()
    except Exception as e:
        logger.warning(str(e))


async def create_user(db: AsyncSession, user: schemas.UserSchemas):
    try:
        rate_and_service: rate_schemas.RateSchemas = await get_rates_by_id(db, user.rate_id.id)
        new_user = models.User(
            name=user.name,
            surname_name=user.surname_name,
            patronymic=user.patronymic,
            balance=user.balance,
            phone_number=user.phone_number,
            msisdn=user.msisdn,
            rate_id=rate_and_service[0].id,
        )
        db.add(new_user)
        await db.commit()
        return user
    except Exception as e:
        logger.warning(str(e))


async def update_user(db: AsyncSession, user: schemas.UserSchemas):
    # rate_and_service: rate_schemas.RateSchemas = await get_rates_by_id(db, user.rate_id.id)
    update = await db.execute(
        update_execute(models.User)
        .where(models.User.id == user.id)
        .values(
            name=user.name,
            surname_name=user.surname_name,
            patronymic=user.patronymic,
            balance=user.balance,
            phone_number=user.phone_number,
            msisdn=user.msisdn,
            rate_id=user.rate_id.id
        )
        .execution_options(synchronize_session="fetch")
    )
    await db.commit()
    return update.scalar()