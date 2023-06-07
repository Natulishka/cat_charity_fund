from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.models.charity_donation import CharityDonation


class Donation(CharityDonation):
    user_id = Column(Integer, ForeignKey('user.id',
                                         name='fk_donation_user_id_user'))
    comment = Column(Text)
    charity_projects = relationship('CharityProject', 
                                    secondary="charity_donations", 
                                    back_populates='donations')
