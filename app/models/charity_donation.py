from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, Table, ForeignKey

from app.core.db import Base


class CharityDonation(Base):
    
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime(), default=datetime.utcnow)
    close_date = Column(DateTime)


charity_donations = Table('charity_donations', Base.metadata,
    Column('charity_project_id', ForeignKey('charityproject.id'), 
           primary_key=True),
    Column('donation_id', ForeignKey('donation.id'), primary_key=True)
)
