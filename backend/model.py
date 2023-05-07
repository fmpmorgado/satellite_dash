from pydantic import BaseModel

class Satellite(BaseModel):
	name: str
	tle1: str
	tle2: str
	epoch_tle: str
	id: str