from typing import Optional

from models.reviews import Review
from schemas.reviews import ReviewAPI, ReviewDB
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


def get_metric(is_negative, is_positive) -> float:
    """
    Высчитывает метрику по формуле.
    """
    total = len(is_negative) + len(is_positive)
    return len(is_positive) / total


async def create_new_review(
    new_review: ReviewAPI,
    session: AsyncSession,
) -> Review:
    """
    Функция для создания нового объекта.
    """
    new_data = new_review.dict()
    db_review = Review(**new_data)
    session.add(db_review)
    await session.commit()
    await session.refresh(db_review)
    return db_review


async def get_list_metric_by_tag_id(
    session: AsyncSession,
) -> Optional[dict[int, float]]:
    """
    Функция для получения метрики для всех тэгов.
    """
    db_review_id = await session.execute(select(Review.tag_id))
    tags = set(db_review_id.scalars().all())
    metrics = {}
    for tag in tags:
        res = await get_metric_by_id(tag, session)
        metrics[tag] = res
    return metrics


async def get_metric_by_id(
    tag_id: int,
    session: AsyncSession,
) -> Optional[float]:
    """
    Функция для создания нового объекта.
    """
    db_review_positive = await session.execute(
        select(Review).where(Review.tag_id == tag_id).where(Review.is_positive == True)
    )
    db_review_positive = db_review_positive.scalars().all()
    db_review_negative = await session.execute(
        select(Review).where(Review.tag_id == tag_id).where(Review.is_negative == True)
    )
    db_review_negative = db_review_negative.scalars().all()
    metric = get_metric(db_review_negative, db_review_positive)
    return metric


async def get_metric_general(
    session: AsyncSession,
) -> Optional[float]:
    """
    Функция для получения метрики по всем объектам.
    """
    db_review_is_positive_all = await session.execute(
        select(Review).where(Review.is_positive == True)
    )
    db_review_is_positive_all = db_review_is_positive_all.scalars().all()
    print(db_review_is_positive_all)
    db_review_is_negative_all = await session.execute(
        select(Review).where(Review.is_negative == True)
    )
    db_review_is_negative_all = db_review_is_negative_all.scalars().all()
    total_metric = get_metric(db_review_is_negative_all, db_review_is_positive_all)
    return total_metric
