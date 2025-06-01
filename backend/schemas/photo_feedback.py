from pydantic import BaseModel


class PhotoFeedback(BaseModel):
    attractiveness_level: int
    attractiveness_reason: str
    pros: list[str]
    to_fix: list[str]
    description: str
