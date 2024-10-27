from pydantic import BaseModel
from datetime import datetime

class TripDataModel(BaseModel):
    datasource: str
    region: str
    origin_coord: str # Convert later for Lat, Long type
    destination_coord: str
    datetime: datetime

    class Config:
        orm_mode = True
