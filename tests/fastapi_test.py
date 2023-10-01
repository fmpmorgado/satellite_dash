import sys
import os
import requests
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient

# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from satellite_test import sat_entry
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_assert_pytest():
    assert 1 == 1

def test_read_test_route():
    response = client.get("/test_route")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

#TODO
"""
@pytest.mark.asyncio
async def test_post_route(client: AsyncClient):
    response = await client.post("/satellites/", json = sat_entry)
    assert response.status_code == 200
    assert response.json() == sat_entry

@pytest.mark.asyncio
def test_get_route():
    pass

@pytest.mark.asyncio
def test_put_route():
    pass

@pytest.mark.asyncio
async def test_delete_route():
    response = client.delete("/satellites/"+str(sat_entry["_id"]))
    assert response.status_code == 200
"""