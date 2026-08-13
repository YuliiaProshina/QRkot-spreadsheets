from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_closed_project_or_invested_project,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import invest

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get('/', response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_charity_projects(session: SessionDep):
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post('/', response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)]
             )
async def create_new_charity_project(charity_project: CharityProjectCreate,
                                     session: SessionDep):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    free_donations = (
        await donation_crud.get_free_donations(
            session=session,
        )
    )
    invest(
        target=new_project,
        sources=free_donations,
    )

    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch('/{project_id}', response_model=CharityProjectDB,
              response_model_exclude_none=True,
              dependencies=[Depends(current_superuser)])
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: SessionDep,
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if obj_in.name is not None and obj_in.name != charity_project.name:
        await check_name_duplicate(obj_in.name, session)
    if (obj_in.full_amount is not None and
            obj_in.full_amount < charity_project.invested_amount):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                'Нельзя установить значение full_amount меньше '
                'уже вложенной суммы.'
            ),
        )
    charity_project = await charity_project_crud.update(charity_project,
                                                        obj_in, session)
    if charity_project.full_amount == charity_project.invested_amount:
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.delete('/{project_id}', response_model=CharityProjectDB,
               response_model_exclude_none=True,
               dependencies=[Depends(current_superuser)]
               )
async def remove_charity_project(
        project_id: int,
        session: SessionDep,

):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    if charity_project is not None:
        await check_closed_project_or_invested_project(project_id, session)
    charity_project = await charity_project_crud.remove(charity_project,
                                                        session)
    return charity_project
