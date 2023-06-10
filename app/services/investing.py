from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def close_object(object: Union[Donation, CharityProject]) -> None:
    object.invested_amount = object.full_amount
    object.fully_invested = True
    object.close_date = datetime.utcnow()


async def investing(
        new_object: Union[Donation, CharityProject],
        session: AsyncSession,
) -> Union[Donation, CharityProject]:
    if type(new_object) == Donation:
        model = CharityProject
    else:
        model = Donation
    alterable_objects = await session.execute(select(model).where(
        model.fully_invested == false()).order_by(model.create_date))
    alterable_objects = alterable_objects.scalars().all()
    for alterable_object in alterable_objects:
        not_invested_amount_new_object = (new_object.full_amount -
                                          new_object.invested_amount)
        not_invested_amount_alterable_object = (
            alterable_object.full_amount -
            alterable_object.invested_amount)
        if (not_invested_amount_new_object >
                not_invested_amount_alterable_object):
            await close_object(alterable_object)
            new_object.invested_amount += not_invested_amount_alterable_object
        else:
            if (not_invested_amount_new_object ==
                    not_invested_amount_alterable_object):
                await close_object(alterable_object)
            else:
                alterable_object.invested_amount += (
                    not_invested_amount_new_object)
            await close_object(new_object)
            break
    session.add_all([new_object, *alterable_objects])
    await session.commit()
    await session.refresh(new_object)
    return new_object
