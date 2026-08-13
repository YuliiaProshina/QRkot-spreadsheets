from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class Donation(CommonMixin, Base):
    comment: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'user.id', name='fk_donation_user_id_users'), nullable=True)
