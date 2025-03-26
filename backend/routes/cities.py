from fastapi import APIRouter

from schemas.city import City
from schemas.district import District, DistrictOutput

router = APIRouter(prefix="/cities")


@router.get("/")
async def get_cities() -> list[City]:
    return [
        City(name="Kraków"),
        City(name="Warszawa"),
        City(name="Wroclaw"),
        City(name="Gdańsk"),
    ]


@router.get("/{city_name}")
async def get_city(city_name: str) -> list[DistrictOutput]:
    city = City(name=city_name)
    return [
        DistrictOutput.model_validate(
            District(city=city, name="Stare Miasto").model_dump()
        ),
        DistrictOutput.model_validate(
            District(city=city, name="Krowodrza").model_dump()
        ),
        DistrictOutput.model_validate(
            District(city=city, name="Podgórze").model_dump()
        ),
    ]
