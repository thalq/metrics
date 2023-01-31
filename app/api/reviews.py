import csv
from typing import List, Optional, Union

import pandas as pd
from core.db import get_async_session
from crud.reviews import (create_new_review, get_list_metric_by_tag_id,
                          get_metric_by_id, get_metric_general)
from fastapi import APIRouter, Depends
from models.reviews import Review
from schemas.reviews import ReviewAPI, ReviewDB
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


def read_file():
    """
    Читает данные из файла .csv.
    """
    file_reader = pd.read_csv("reviews_sentiments_202301301810.csv", delimiter=';')
    return file_reader


@router.post(
    '/create',
    response_model_exclude_none=True,
)
async def create_review_list(
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """
    Добавляет данные из файла .csv в базу данных.
    """
    file_reader = read_file()
    for i in range (0, len(file_reader)):
        row = file_reader.iloc[i].to_dict()
        db_review = Review(**row)
        session.add(db_review)
        await session.commit()
        await session.refresh(db_review)


@router.post(
    "/",
    response_model=ReviewDB,
    response_model_exclude_none=True,
)
async def create_review(
    review: ReviewAPI,
    session: AsyncSession = Depends(get_async_session),
) -> ReviewDB:
    """
    Создает новый объект.
    """
    return await create_new_review(review, session)


@router.get(
    "/metric",
    response_model=Union[float, List[ReviewDB], dict[int, float]],
    response_model_exclude_none=True,
)
async def get_metric(
    tag_id: Optional[Union[int, str]] = None,
    session: AsyncSession = Depends(get_async_session),
) -> Union[float, dict[int, float]]:
    """
    Если не указан tag_id, возвращает метрику по всему файлу,
    если tag_id равен all, возвращает словарь тэг: метрика,
    если тэк равен числу, возвращает метрику конкретного тега.
    """
    if tag_id is not None and isinstance(tag_id, int):
        return await get_metric_by_id(tag_id, session)

    if tag_id == "all":
        return await get_list_metric_by_tag_id(session)

    return await get_metric_general(session)
