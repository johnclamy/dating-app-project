from enum import Enum


# --- Enums for dating choices ---
class LookinFor(str, Enum):
    RELATIONSHIP = "relationship"
    FRIENDSHIP = "friendship"
    CASUAL = "casual"
    NETWORKING = "family"
