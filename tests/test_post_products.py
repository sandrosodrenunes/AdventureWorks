import pytest
import httpx
import subprocess
import time
from app.main import app
from app.models import Product

@pytest.fixture(scope="module")
def client():
    server_process = subprocess.Popen(["uvicorn", "app.main:app", "--port", "8001"])
    time.sleep(5)  

    async_client = httpx.AsyncClient(base_url="http://localhost:8001")
    
    yield async_client

    server_process.terminate()

@pytest.mark.asyncio
async def test_create_product(client):
    product_data = {
        "ProductID": 100,
        "Name": "Adjustable teste",
        "ProductNumber": "AR-5382",
        "MakeFlag": 0,
        "FinishedGoodsFlag": 0,
        "Color": None,
        "SafetyStockLevel": 1000,
        "ReorderPoint": 750,
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
    }

    response = await client.post("/products/", json=product_data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["ProductID"] == 100
    assert response_data["Name"] == "Adjustable teste"


