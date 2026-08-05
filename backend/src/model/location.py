from pydantic import BaseModel, Field


# --- Nested schema for API request/response ---
class Location(BaseModel):
    """
    Represents a geographic point. 
    SpatiaLite uses X (Longitude) and Y (Latitude),
    so when generating WKT: POINT(longitude latitude)
    """
    latitude: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Y coordinate",
    )

    longitude: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="X coordinate",
    )
