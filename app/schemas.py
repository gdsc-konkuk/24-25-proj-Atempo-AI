from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    latitude: float
    longitude: float

class RequestModel(BaseModel):
    location: Location
    search_radius: int
    patient_condition: str

class Hospital(BaseModel):
    name: str
    phone_number: str
    address: str
    distance: str
    travel_time: str
    departments: List[str]