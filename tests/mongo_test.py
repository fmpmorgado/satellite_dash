import sys
import os
import asyncio
import pytest
import copy

# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from satellite_test import sat_entry
from backend.database import fetch_one_satellite, create_satellite, fetch_all_satellite, delete_satellite, update_satellite

# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

@pytest.mark.asyncio
async def test_new_satellite():
    """
    Test MongoDB post using mock satellite
    """

    response = await create_satellite(sat_entry)
    assert response == sat_entry

@pytest.mark.asyncio
async def test_find_satellite():
    """
    Test MongoDB get using mock satellite
    """

    response = await fetch_one_satellite(sat_entry["_id"])
    assert response == sat_entry

@pytest.mark.asyncio
async def test_update_satellite():
    """
    Test MongoDB update using mock satellite
    """
    
    sat_entry2 = copy.deepcopy(sat_entry)
    sat_entry2["name"] = ["Test another satellite"]
    response = await update_satellite(sat_entry["_id"], sat_entry2)
    assert response == sat_entry2

@pytest.mark.asyncio
async def test_delete_satellite():
    """
    Test MongoDB delete using mock satellite
    """

    response = await delete_satellite(sat_entry["_id"])
    assert response == True
