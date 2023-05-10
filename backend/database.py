import motor.motor_asyncio
from backend.model import Satellite

# Client object to access database
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongodb:27017')

database = client.tracker
collection = database.satellite

async def fetch_one_satellite(id):
	document = await collection.find_one({"_id": id})
	return document

async def create_satellite(satellite):
	document = satellite
	result = await collection.insert_one(document)
	return document

async def fetch_all_satellite():
	satellite = []
	async for document in collection.find():
		satellite.append(Satellite(**document))
	return satellite

async def delete_satellite(id: str):
	result = await collection.find_one({"_id":id})
	if result:
		await collection.delete_one({"_id": id})
		return True
	return False
