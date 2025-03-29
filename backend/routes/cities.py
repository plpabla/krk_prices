from fastapi import APIRouter

from schemas.city import City
from schemas.district import District, DistrictOutput
from model import model

router = APIRouter(prefix="/cities")


@router.get("/")
async def get_cities() -> list[City]:
    return [
        City(name="Kraków"),
    ]


@router.get("/{city_name}")
async def get_city(city_name: str) -> list[DistrictOutput]:
    city = City(name=city_name)

    return [
        DistrictOutput.model_validate(District(city=city, name=name).model_dump())
        for name in model.get_districts()
    ]
