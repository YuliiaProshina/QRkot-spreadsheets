from datetime import datetime
from typing import Iterable, Union

from app.models.charity_project import CharityProject
from app.models.donation import Donation

InvestmentObject = Union[CharityProject, Donation]


def close_investment_object(obj: InvestmentObject) -> None:
    """Проверяет закрытые проекты и сохраняет дату закрытия."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


def invest(
    target: InvestmentObject,
    sources: Iterable[InvestmentObject],
) -> InvestmentObject:
    """Распределяет донаты между проектами.
    Донаты последовательно переносятся из 'source' в 'target'.
    Полностью инвестированные проекты закрываются автоматически.
    """
    for source in sources:
        target_free_amount = target.full_amount - target.invested_amount
        source_free_amount = source.full_amount - source.invested_amount
        investment_amount = min(target_free_amount, source_free_amount)
        target.invested_amount += investment_amount
        source.invested_amount += investment_amount
        if source.invested_amount == source.full_amount:
            close_investment_object(source)
        if target.invested_amount == target.full_amount:
            close_investment_object(target)
            break
    return target