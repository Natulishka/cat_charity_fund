from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt, Field, root_validator, validator


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DontionDB(DonationBase):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
