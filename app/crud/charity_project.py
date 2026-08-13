from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(select(
            CharityProject.id).where(
            CharityProject.name == charity_project_name))
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_open_projects(self,
                                session: AsyncSession) -> list[CharityProject]:
        open_project = await session.execute(select(CharityProject).where(
            CharityProject.fully_invested.is_(False)).order_by(
            CharityProject.create_date))
        return list(open_project.scalars().all())

    async def get_projects_by_completion_rate(self, session: AsyncSession) -> list[CharityProject]:
        close_project = await session.execute(select(CharityProject).where(
            CharityProject.fully_invested.is_(True)).order_by(
            CharityProject.create_date))
        return list(close_project.scalars().all())


charity_project_crud = CRUDCharityProject(CharityProject)
