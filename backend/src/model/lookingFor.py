from enum import Enum


# --- Enums for dating choices ---
class LookingFor(str, Enum):
    RELATIONSHIP = "relationship"
    CASUAL = "casual"
    FRIENDSHIP = "friendship"
    NETWORKING = "networking"
