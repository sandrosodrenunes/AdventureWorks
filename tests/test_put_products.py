# tests/test_update_product.py

import pytest
import httpx
import asyncio
import subprocess
from app.main import app

def start_server():
    return subprocess.Popen(["uvicorn", "app.main:app", "--port", "8001"])

@pytest.fixture(scope="module")
def client():
    server_process = start_server()
    asyncio.sleep(5)  # Aguarda o servidor iniciar

    async_client = httpx.AsyncClient(base_url="http://localhost:8001")

    yield async_client

    server_process.terminate()

@pytest.mark.asyncio
async def test_update_product(client):
    response = await client.put("/products/100", json={
        "ProductID": 100,
        "Name": "Updated Adjustable teste",
        "ProductNumber": "AR-5382-UPDATED",
        "MakeFlag": 0,
        "FinishedGoodsFlag": 0,
        "Color": None,
        "SafetyStockLevel": 2000,
        "ReorderPoint": 1500,
        "StandardCost": 0,
        "ListPrice": 0,
        "Size": None,
        "SizeUnitMeasureCode": None,
        "WeightUnitMeasureCode": None,
        "Weight": None,
        "DaysToManufacture": 0,
        "ProductLine": None,
        "Class": None,
        "Style": None,
        "ProductSubcategoryID": None,
        "ProductModelID": None,
        "SellStartDate": "2008-04-30T00:00:00",
        "SellEndDate": None,
        "DiscontinuedDate": None,
        "rowguid": "694215b7-08f7-4c0d-acb1-d734ba44c0c9",
        "ModifiedDate": "2014-02-08T10:01:36.827000"
    })

    assert response.status_code == 200
    updated_product = response.json()
    assert updated_product["ProductID"] == 100
    assert updated_product["Name"] == "Updated Adjustable teste"
    assert updated_product["ProductNumber"] == "AR-5382-UPDATED"
