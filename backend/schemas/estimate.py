from pydantic import BaseModel
from enum import Enum


class StateType(str, Enum):
    READY_TO_MOVE = "READY_TO_MOVE"
    NEEDS_RENOVATION = "NEEDS_RENOVATION"
    NEEDS_FINISHING = "NEEDS_FINISHING"


class HeatingType(str, Enum):
    DISTRICT = "DISTRICT"
    GAS = "GAS"
    ELECTRIC = "ELECTRIC"
    OTHER = "OTHER"


class MarketType(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"


class OwnershipType(str, Enum):
    OWNERSHIP = "OWNERSHIP"
    COOPERATIVE = "COOPERATIVE"
    OTHER = "OTHER"


class AdType(str, Enum):
    PRIVATE = "PRIVATE"
    AGENCY = "AGENCY"


class AvailableType(str, Enum):
    NOW = "NOW"
    Y2025 = "Y2025"
    Y2026 = "Y2026"
    Y2027 = "Y2027"
    Y2028 = "Y2028"


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

    rent: float | None = None
    extra_info: str


class EstimateOutput(BaseModel):
    price: int
