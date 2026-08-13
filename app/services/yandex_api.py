from datetime import timedelta


def format_time_delta(time_delta: timedelta) -> str:
    """Вычисляет количество дней, часов и минут."""
    days = time_delta.days
    hours = time_delta.seconds // 3600
    minutes = (time_delta.seconds // 60) % 60
    if days:
        return f'{days} дн. {hours} ч.'
    return f'{hours} ч. {minutes} мин.'


async def create_simple_report(file_path: str, upload_url: str, yandex_client: YandexDiskClient,
                               folder: str = "Reports"):
    now_date_time = datetime.now().strftime(settings.report_format)
    safe_filename = f"Отчет_{now_date_time}".replace(':', '-').replace(' ', '_').replace('/', '-')
    upload_url, file_path = await yandex_client.create_simple_report(safe_filename, folder)
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet("Отчет")
    title_format = workbook.add_format({'bold': True, 'font_size': 14})
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#2F75B5',
        'font_color': 'white',
        'border': 1,
        'align': 'center'
    })
    cell_format = workbook.add_format({'border': 1, 'align': 'center'})
    worksheet.merge_range('A1:B1', f"Отчет от {now_date_time}", title_format)
    headers = ['Название проекта', 'Время сбора', 'Описание']
    for col, header in enumerate(headers):
        worksheet.write(1, col, header, header_format)
    for row, res in enumerate(reservations, start=2):
        worksheet.write(row, 0, str(res['charity_project_name']), cell_format)
        worksheet.write(row, 1, str(res[format_time_delta()]), cell_format)
        worksheet.write(row, 2, str(res['charity_project_description']), cell_format)
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 25)
    workbook.close()
    output.seek(0)
    await yandex_client.upload_file(upload_url, output.getvalue())
    return await yandex_client.publish_file(file_path)




