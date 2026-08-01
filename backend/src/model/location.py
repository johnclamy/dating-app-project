from pydantic import BaseModel


# --- Nested Model for SpatiaLite Location ---
class Location(BaseModel):
    """
    Represents a geographic point. 
    Note: SpatiaLite uses X (Longitude) and Y (Latitude).
    """
    latitude: float
    longitude: float

