from pydantic import BaseModel


class PhotoFeedback(BaseModel):
    luxury_level: int
    pros: list[str]
    to_fix: list[str]
    description: str
