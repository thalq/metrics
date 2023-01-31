from sqlalchemy import BigInteger, Boolean, Column, Float, Integer, String

from core.db import Base


class Review(Base):
    review_id = Column(BigInteger)
    tag_id = Column(Integer)
    date_publish = Column(String)
    rating = Column(Float)
    sentiment_score = Column(Integer)
    is_positive = Column(Boolean)
    is_negative = Column(Boolean)
    is_neutral = Column(Boolean)
