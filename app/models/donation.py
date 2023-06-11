from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.charity_donation import CharityDonation


class Donation(CharityDonation):
    user_id = Column(Integer, ForeignKey('user.id',
                                         name='fk_donation_user_id_user'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Пожертвование на сумму {self.full_amount}'
        )