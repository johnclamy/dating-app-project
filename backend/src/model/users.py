import uuid
from datetime import date, datetime
from pydantic import BaseModel
from model.gender import Gender
from model.lookingFor import LookingFor
from model.location import Location


# --- Main User Model ---
class User(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    date_of_birth: date 
    email: str
    gender: Gender
    looking_for: LookingFor
    location: Location
    bio: str | None
    created_at: datetime
    updated_at: datetime    
