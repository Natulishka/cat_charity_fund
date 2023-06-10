from typing import List


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donations_crud
from app.schemas.donations import (DonationBase, DontionDB)
from app.models import User


RESPONSE_MODEL_EXCLUDE = {
    'user_id', 'invested_amount', 'fully_invested', 'close_date'
    }
router = APIRouter()


@router.post('/', 
             response_model=DontionDB,
             response_model_exclude_none=True,
             response_model_exclude=RESPONSE_MODEL_EXCLUDE,
             )
async def create_donation(
        donation: DonationBase,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    '''Сделать пожертвование.'''
    new_donation = await donations_crud.create(
        donation, session, user
    )
    return new_donation


@router.get(
    '/',
    response_model=List[DontionDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    '''Только для суперюзеров. \n
    Получает список всех пожертвований.'''
    donations = await donations_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DontionDB],
    response_model_exclude_none=True,
    response_model_exclude=RESPONSE_MODEL_EXCLUDE,
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    '''Получить список моих пожертвований.'''
    donations = await donations_crud.get_by_user(session, user)
    return donations
