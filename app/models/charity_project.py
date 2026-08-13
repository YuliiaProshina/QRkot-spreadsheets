from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import STRING_MAX_LENGTH
from app.core.db import Base, CommonMixin


class CharityProject(CommonMixin, Base):
    name: Mapped[str] = mapped_column(String(STRING_MAX_LENGTH), unique=True,
                                      nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
