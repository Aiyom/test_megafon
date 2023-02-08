import asyncio

from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from rate import schemas


async def validate_price(price):
    if price <= 0.0:
        return False
    return True