from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.charity_donation import CharityDonation


class CharityProject(CharityDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    # donations = relationship('Donation',
    #                          secondary="charity_donations",
    #                          back_populates='charity_projects')
