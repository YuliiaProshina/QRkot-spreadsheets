from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков'
    app_description: str = ('Собирает пожертвования на всевозможные задачи, '
                            'связанные с помощью кошачьей популяции:'
                            ' на корм, на медицинское обслуживание, '
                            'организацию приютов и на другую помощь котам, '
                            'кошкам и котятам.')
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    yandex_disk_token: Optional[str] = None
    report_format: str = '%Y/%m/%d %H:%M:%S'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
