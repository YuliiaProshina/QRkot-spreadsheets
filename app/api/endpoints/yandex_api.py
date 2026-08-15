from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.core.yandex_client import YandexDiskClient, get_yandex_client
from app.crud.charity_project import charity_project_crud
from app.services.yandex_api import create_simple_report

router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],
    summary='Создать Excel-отчёт на Яндекс Диске',
    description=""""
    Создаёт Excel-файл с отчётом по завершённым проектам.
    Файл сохраняется на Яндекс Диске в папке 'Reports'
    и становится доступен по публичной ссылке.

    Требуются права суперпользователя.
    """
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        yandex_client: YandexDiskClient = Depends(get_yandex_client)
) -> str:
    """
    Создание отчёта в Excel-файле на Яндекс Диске
    """
    charity_projects = await (
        charity_project_crud.get_projects_by_completion_rate(
            session=session
        ))
    if not charity_projects:
        raise HTTPException(
            status_code=404,
            detail='Нет данных для формирования отчёта'
        )
    try:
        public_url = await create_simple_report(charity_projects,
                                                yandex_client)
        return public_url
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Ошибка при создании отчёта: {str(e)}'
        )
