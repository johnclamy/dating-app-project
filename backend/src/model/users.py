import uuid
from datetime import date, datetime
from pydantic import BaseModel


# --- Main User Model ---
class User(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    date_of_birth: date 
    email: str
    gender: str
    looking_for: str
    location: str
    bio: str
    created_at: datetime
    updated_at: datetime    
