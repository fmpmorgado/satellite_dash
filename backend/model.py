from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Satellite(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    name: str = Field(...)
    tle1: str = Field(...)
    tle2: str = Field(...)
    epoch_tle: str = Field(...)

    class Config:
        allow_population_by_field_name = True

class UpdateSatellite(BaseModel):
    name: Optional[str]
    tle1: Optional[str]
    tle2: Optional[str]
    epoch_tle: Optional[str]

def string_to_date(date: str):
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
