from pydantic import BaseModel
from typing import List

class Location(BaseModel):
    latitude: float # 위도
    longitude: float # 경도

class RequestModel(BaseModel):
    location: Location
    search_radius: int # 검색 반경 (미터 단위)
    patient_condition: str

class Hospital(BaseModel):
    name: str
    phone_number: str
    address: str
    distance: str
    travel_time: str
    departments: List[str]