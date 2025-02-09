from dataclasses import dataclass
from typing import Optional, ClassVar, List


@dataclass
class RealEstateListing:
    """Represents a single real estate listing from OtoDom."""

    # Default value for missing information
    MISSING_INFO: ClassVar[str] = "brak informacji"

    # Identification
    slug: str
    url: str
    name: str

    # Basic information
    price: Optional[float]
    area: Optional[float]
    rooms: str
    build_year: Optional[int]  # Year of construction
    elevator: bool  # Whether the building has an elevator
    location: List[str]  # Location components (district, area, etc.)
    location_lat: Optional[float]  # Latitude coordinate
    location_lon: Optional[float]  # Longitude coordinate

    # Property characteristics
    heating: str
    floor: str
    rent: Optional[float]
    state: str  # Construction status/finishing state
    market: str  # Primary/Secondary market
    ownership: str  # Form of ownership

    # Additional information
    available: str
    ad_type: str  # Type of advertiser
    extra_info: str  # Additional features and information

    @property
    def price_per_meter(self) -> Optional[float]:
        """Calculate price per square meter if both price and area are available."""
        if self.price and self.area and self.area > 0:
            return self.price / self.area
        return None

    @classmethod
    def create_empty(cls, url: str) -> "RealEstateListing":
        """Create an empty listing with default values."""
        return cls(
            slug=url.split("/")[-1],
            url=url,
            name=cls.MISSING_INFO,
            price=None,
            area=None,
            rooms=cls.MISSING_INFO,
            build_year=None,
            elevator=False,
            location=[],
            location_lat=None,
            location_lon=None,
            heating=cls.MISSING_INFO,
            floor=cls.MISSING_INFO,
            rent=None,
            state=cls.MISSING_INFO,
            market=cls.MISSING_INFO,
            ownership=cls.MISSING_INFO,
            available=cls.MISSING_INFO,
            ad_type=cls.MISSING_INFO,
            extra_info=cls.MISSING_INFO,
        )
