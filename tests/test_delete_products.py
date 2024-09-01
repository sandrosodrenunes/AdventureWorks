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
async def test_delete_product(client):
    # Primeiro, crie um produto para garantir que exista um produto para excluir.
    create_response = await client.post("/products/", json={
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
    })

    #assert create_response.status_code == 200


    delete_response = await client.delete("/products/100")
    assert delete_response.status_code == 204


    get_response = await client.get("/products/100")
    assert get_response.status_code == 404  

