import io
from datetime import datetime, timedelta

import pandas as pd

from app.core.config import settings
from app.core.yandex_client import YandexDiskClient


def format_time_delta(time_delta: timedelta) -> str:
    """Вычисляет количество дней, часов и минут."""
    days = time_delta.days
    hours = time_delta.seconds // 3600
    minutes = (time_delta.seconds // 60) % 60
    if days:
        return f'{days} дн. {hours} ч.'
    return f'{hours} ч. {minutes} мин.'


async def create_simple_report(charity_projects,
                               yandex_client: YandexDiskClient,
                               folder: str = 'Reports'):
    now_date_time = datetime.now().strftime(settings.report_format)
    safe_filename = f'Отчет_{now_date_time}'.replace(':', '-').replace(
        ' ', '_').replace('/', '-')
    upload_url, file_path = await yandex_client.create_excel_file(
        safe_filename, folder)
    data = [
        {
            'Название проекта': project.name,
            'Время сбора': format_time_delta(
                project.close_date - project.create_date
            ),
            'Описание': project.description,
        }
        for project in charity_projects
    ]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(
            writer,
            sheet_name='Отчет',
            startrow=1,
            index=False,
        )
        workbook = writer.book
        worksheet = writer.sheets['Отчет']
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
        })
        worksheet.merge_range(
            'A1:C1',
            f'Отчет от {now_date_time}',
            title_format,
        )
        total_row = len(df) + 2
        worksheet.write(
            total_row,
            0,
            f'Всего проектов: {len(df)}',
        )
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 50)
    workbook.close()
    output.seek(0)
    await yandex_client.upload_file(upload_url, output.getvalue())
    return await yandex_client.publish_file(file_path)
