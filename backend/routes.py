from fastapi import HTTPException, WebSocket, APIRouter
from . import model
import asyncio
from backend.database import fetch_one_satellite, create_satellite, fetch_all_satellite

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
async def read_satellite_by_id(id):
	response = await fetch_one_satellite(id)
	if response:
		return response
	raise HTTPException(404, "There is no TODO item with this title")


@route.get("/satellites")
async def get_todo():
	response = await fetch_all_satellite()
	return response


@route.post("/satellites", response_model = model.Satellite)
async def post_satellite(satellite: model.Satellite):
	response = await create_satellite(satellite.dict())
	if response:
		return response
	raise HTTPException(400, "Bad request")
