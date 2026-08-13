from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core.constants import (DESCRIPTION_MIN_LENGTH, STRING_MAX_LENGTH,
                                STRING_MIN_LENGTH)


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=STRING_MIN_LENGTH,
                      max_length=STRING_MAX_LENGTH)
    description: str = Field(..., min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: PositiveInt
    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=STRING_MIN_LENGTH,
        max_length=STRING_MAX_LENGTH,
    )
    description: Optional[str] = Field(
        None,
        min_length=DESCRIPTION_MIN_LENGTH,
    )
    full_amount: Optional[PositiveInt] = None


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
