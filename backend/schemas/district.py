from pydantic import BaseModel
from .city import City


class District(BaseModel):
    city: City
    name: str


class DistrictOutput(BaseModel):
    name: str
