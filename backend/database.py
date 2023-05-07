import motor.motor_asyncio
from backend.model import Satellite

# Client object to access database
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongodb:27017')

database = client.tracker
collection = database.satellite

async def fetch_one_satellite(id):
	document = await collection.find_one({"id":id})
	return document

async def create_satellite(satellite):
	document = satellite
	print(document)
	result = await collection.insert_one(document)
	return document

async def fetch_all_satellite():
	satellite = []
	cursor = collection.find({})
	async for document in cursor:
		satellite.append(Satellite(**document))
	return satellite