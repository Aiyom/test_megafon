
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.database import get_session
from user.crud import *
from user.schemas import UserSchemas
from user.validate import check_balance_when_edit_rate_or_service

router = APIRouter()


@router.get('/users/{phone_number}', status_code=status.HTTP_200_OK)
async def get_users(phone_number: str, db: AsyncSession = Depends(get_session)) -> dict:
    users = await get_user_by_phone_number(db, phone_number)
    return {"users": users}


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_session), limit: int = 10, page: int = 1, search: str = '') -> dict:
    skip = (page - 1) * limit
    users = await get_all_users(db, search, limit, skip)
    return {'count': len(users), "users": users}


@router.post('/users', status_code=status.HTTP_201_CREATED)
async def create_users(user: UserSchemas, db: AsyncSession = Depends(get_session)):
    db_user = await get_user_by_phone_number(db, phone_number=user.phone_number)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    new_user = await create_user(db, user)
    return {"status": "success", "user": new_user}


@router.patch('/users', status_code=status.HTTP_200_OK)
async def update_users(user: UserSchemas, db: AsyncSession = Depends(get_session)):
    await check_balance_when_edit_rate_or_service(db, user)
    db_user = await get_user_by_phone_number(db, phone_number=user.phone_number)
    if not db_user:
        raise HTTPException(status_code=400, detail=f"{user.name} is not exist")
    await update_user(db, user)
    return {"status": "success", "user": user}

