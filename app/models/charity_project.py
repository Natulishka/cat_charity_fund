from sqlalchemy import Column, String, Text

from app.models.charity_donation import CharityDonation


class CharityProject(CharityDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
