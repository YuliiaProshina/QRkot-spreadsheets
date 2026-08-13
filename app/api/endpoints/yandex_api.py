from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.core.yandex_client import YandexDiskClient, get_yandex_client



router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)],
    summary="Создать Excel-отчёт на Яндекс Диске",
    description="""
    Создаёт Excel-файл с отчётом по бронированиям переговорок.
    Файл сохраняется на Яндекс Диске в папке "Reports"
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
    from_date = datetime(2000, 1, 1)
    to_date = datetime.now() + timedelta(days=365 * 100)
    charity_projects = await charity_project_crud.get_projects_by_completion_rate(
        from_reserve=from_date,
        to_reserve=to_date,
        session=session
    )
    if not charity_projects:
        raise HTTPException(
            status_code=404,
            detail="Нет данных для формирования отчёта"
        )
    try:
        public_url = await create_simple_report(upload_url, charity_projects, yandex_client)
        return public_url
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при создании отчёта: {str(e)}"
        )