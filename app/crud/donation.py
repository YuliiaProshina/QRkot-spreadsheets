from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):
    async def get_free_donations(
        self,
        session: AsyncSession,
    ) -> list[Donation]:
        result = await session.execute(
            select(Donation)
            .where(
                Donation.fully_invested.is_(False)
            )
            .order_by(Donation.create_date)
        )

        return list(result.scalars().all())

    async def get_by_user(
            self, session: AsyncSession, user: User
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
