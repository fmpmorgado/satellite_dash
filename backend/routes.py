from fastapi import HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from . import model
import asyncio
from backend.database import fetch_one_satellite, create_satellite, fetch_all_satellite, delete_satellite
from typing import List

route = APIRouter()

@route.get("/")
def read_main():
    return {
        "routes": [
            {"method": "GET", "path": "/", "summary": "Landing"},
            {"method": "GET", "path": "/dash", "summary": "Sub-mounted Dash application"},
        ]
    }

@route.get("/satellites/{id}", response_model = model.Satellite)
async def read_satellite_by_id(id: str):
	response = await fetch_one_satellite(id)
	if response:
		return response
	raise HTTPException(404, "There is no item with this ID")


@route.get("/satellites", response_model = List[model.Satellite])
async def get_satellites():
	response = await fetch_all_satellite()
	return response

@route.post("/satellites", response_model = model.Satellite)
async def post_satellite(satellite: model.Satellite ):
	satellite = jsonable_encoder(satellite)
	response = await create_satellite(satellite)
	if response:
		return response
	raise HTTPException(400, "Bad request")

@route.delete('/satellites/{id}')
async def delete_satellite_by_id(id: str):
	response = await delete_satellite(id)
	if response:
		return "Deleted the satellite"
	raise HTTPException(404, "There is no satellite item with this title")
