from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]
    
    class Config:
        extra = Extra.forbid
    
    @validator('name')
    def name_cannot_be_null_or_more_100(cls, value):
        if value is None or value == '':
            raise ValueError('Имя проекта не может быть пустым!')
        if len(value) > 100:
            raise ValueError('Длина проекта не может быть больше 100 символов!')
        return value
    
    @validator('description')
    def description_cannot_be_null(cls, value):
        if value is None or value == '':
            raise ValueError('Описание не может быть пустым!')
        return value


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    full_amount: PositiveInt
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
