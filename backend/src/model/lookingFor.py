from enum import Enum


# --- Enums for dating choices ---
class LookingFor(str, Enum):
    RELATIONSHIP = "relationship"
    FRIENDSHIP = "friendship"
    CASUAL = "casual"
    NETWORKING = "family"
