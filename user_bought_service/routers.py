from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.database import get_session
from user.schemas import UserAndCommunicationServiceSchemas
from user.validate import check_balance_when_edit_rate_or_service
from user_bought_service.crud import *

router = APIRouter()


@router.get('/connected/service', status_code=status.HTTP_200_OK, response_model=List[UserAndCommunicationServiceSchemas])
async def get_users(db: AsyncSession = Depends(get_session), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    # users = await get_all_users_service(db, search, limit, skip)
    return await get_all_users_service(db, search, limit, skip)


@router.post('/connected/service', status_code=status.HTTP_201_CREATED)
async def create_users_service(user: UserAndCommunicationServiceSchemas, db: AsyncSession = Depends(get_session)):
    db_user = await get_user_by_phone_number(db, phone_number=user.user_id.phone_number)
    print(db_user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Phone number no registered")
    new_user = await create_user_service(db, user)
    return {"status": "success", "user": new_user}


# @router.patch('/connected/service', status_code=status.HTTP_200_OK)
# async def update_users_service(user: UserAndCommunicationServiceSchemas, db: AsyncSession = Depends(get_session)):
#     await check_balance_when_edit_rate_or_service(db, user.user_id, False)
#     db_user = await get_user_by_phone_number(db, phone_number=user.user_id.phone_number)
#     if not db_user:
#         raise HTTPException(status_code=400, detail=f"{user.user_id.name} is not exist")
#     await update_user_service(db, user)
#     return {"status": "success", "user": user}