from pydantic import BaseModel


class PhotoFeedback(BaseModel):
    luxury_level: int
