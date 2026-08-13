from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investing import invest

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get('/', response_model=list[DonationFullInfoDB],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)])
async def get_all_donations(session: SessionDep):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session=session)
    return donations


@router.post('/', response_model=DonationDB, response_model_exclude_none=True,
             response_model_exclude={'user_id'})
async def create_donation(donation: DonationCreate, session: SessionDep,
                          user: Annotated[User, Depends(current_user)]):
    new_donation = await donation_crud.create(donation, session, user)
    open_projects = (
        await charity_project_crud.get_open_projects(session=session))
    invest(target=new_donation, sources=open_projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get('/my', response_model=list[DonationDB],
            response_model_exclude={'user_id'},
            response_model_exclude_none=True)
async def get_my_donations(session: SessionDep,
                           user: Annotated[User, Depends(current_user)]):
    """Получает список всех донатов для текущего пользователя."""
    donations = await donation_crud.get_by_user(session=session, user=user)
    return donations
