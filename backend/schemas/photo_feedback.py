from pydantic import BaseModel


class PhotoFeedback(BaseModel):
    attractiveness_level: int
    pros: list[str]
    to_fix: list[str]
    description: str
