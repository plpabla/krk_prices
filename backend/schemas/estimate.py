from pydantic import BaseModel
from enum import Enum


class HeatingType(str, Enum):
    DISTRICT = "miejskie"
    GAS = "gazowe"
    ELECTRIC = "elektryczne"
    OTHER = "inne"


class StateType(str, Enum):
    READY_TO_MOVE = "Do zamieszkania"
    NEEDS_RENOVATION = "Do remontu"
    NEEDS_FINISHING = "Do wykończenia"


class MarketType(str, Enum):
    PRIMARY = "Pierwotny"
    SECONDARY = "Wtórny"


class OwnershipType(str, Enum):
    OWNERSHIP = "Własnościowe"
    COOPERATIVE = "Spoldzielcze"
    OTHER = "Inne"


class AdType(str, Enum):
    PRIVATE = "prywatny"
    AGENCY = "biuro"


class AvailableType(str, Enum):
    NOW = "od zaraz"
    Y2025 = "2025"
    Y2026 = "2026"
    Y2027 = "2027"
    Y2028 = "2028+"


class EstimateInput(BaseModel):
    location: str
    city: str
    district: str
    area: float
    rooms: int
    floor: int
    floorsInBuilding: int

    balcony: bool
    separate_kitchen: bool

    state: StateType
    market: MarketType
    ad_type: AdType
    ownership: OwnershipType
    heating: HeatingType
    available: AvailableType

    garage: bool
    elevator: bool
    basement: bool

    rent: float | None = None  # not provided on frontend


class EstimateOutput(BaseModel):
    price: int
