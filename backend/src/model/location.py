from pydantic import BaseModel, Field


# --- Nested Model for SpatiaLite Location ---
class Location(BaseModel):
    """
    Represents a geographic point. 
    Note: SpatiaLite uses X (Longitude) and Y (Latitude).
    """
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Y coordinate")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="X coordinate")

