from pydantic import BaseModel


class ReviewAPI(BaseModel):
    review_id: int
    tag_id: int
    date_publish: str
    rating: float
    sentiment_score: int
    is_positive: bool
    is_negative: bool
    is_neutral: bool


class ReviewDB(ReviewAPI):
    id: int

    class Config:
        orm_mode = True
