from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.donation import Donation


class CRUDReservation(CRUDBase):

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ) -> List[Donation]:
        donations = await session.execute(select(Donation).where(
            Donation.user_id == user.id
        ))
        donations = donations.scalars().all()
        return donations


donations_crud = CRUDReservation(Donation)
