from fastapi import HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse
from . import model
import asyncio
from backend.database import fetch_one_satellite, create_satellite, fetch_all_satellite, delete_satellite, update_satellite
from typing import List

route = APIRouter()

@route.get("/")
def redirect_main():
	return RedirectResponse("/dash")

@route.get("/test_route")
def test_route():
	return {"message": "Hello World"}

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

@route.put("/satellites/{id}]", response_model = model.UpdateSatellite)
async def put_satellite(id: str, satellite: model.UpdateSatellite ):
	satellite = jsonable_encoder(satellite)
	response = await update_satellite(id, satellite)
	if response:
		return response
	raise HTTPException(400, "Bad request")

@route.delete('/satellites/{id}')
async def delete_satellite_by_id(id: str):
	response = await delete_satellite(id)
	if response:
		return "Deleted the satellite"
	raise HTTPException(404, "There is no satellite item with this title")
