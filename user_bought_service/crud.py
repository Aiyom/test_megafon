
from rate.crud import *
from rate import schemas as rate_schemas
from user import models, schemas
from user.crud import get_user_by_phone_number


logger = logging.getLogger(__name__)


async def get_all_users_service(db: AsyncSession, search, limit, skip):
    try:
        users = await db.execute(
            select(models.UserAndCommunicationService, models.RateAndService, models.User)
            .filter(models.User.phone_number.contains(search))
            .filter(models.UserAndCommunicationService.communication_service_id == models.RateAndService.id)
            .filter(models.UserAndCommunicationService.user_id == models.User.id)
            .limit(limit)
            .offset(skip))
        return [dict(result) for result in users.fetchall()]
    except Exception as e:
        logger.warning(str(e))


async def create_user_service(db: AsyncSession, user):
    # try:
        to_add = []
        for item in user.communication_service_id:
            to_add.append(models.UserAndCommunicationService(
            user_id=user.user_id.id,
            communication_service_id=item.id
        ))
        db.add_all(to_add)
        await db.commit()
        return user
    # except Exception as e:
    #     logger.warning(str(e))


async def update_user_service(db: AsyncSession, user: schemas.UserAndCommunicationServiceSchemas):
    user_on_db: rate_schemas.RateSchemas = await get_user_by_phone_number(db, user.user_id.phone_number)
    update = await db.execute(
        update_execute(models.UserAndCommunicationService)
        .where(models.UserAndCommunicationService.id == user.id)
        .values(
            user_id=user.user_id.rate_id.id,
            communication_service_id=user_on_db.id
        )
        .execution_options(synchronize_session="fetch")
    )
    await db.commit()
    return update.scalar()