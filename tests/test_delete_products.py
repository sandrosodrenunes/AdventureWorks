import pytest
import httpx
import time
import subprocess

def start_server():
    return subprocess.Popen(["uvicorn", "app.main:app", "--port", "8001"])

@pytest.fixture(scope="module")
def client():
    server_process = start_server()
    time.sleep(5)  

    
    client = httpx.AsyncClient(base_url="http://localhost:8001")
    
   
    yield client

    
    client.aclose()
    server_process.terminate()
    server_process.wait()

@pytest.mark.asyncio
async def test_delete_product(client):
    delete_response = await client.delete("/products/100")
    assert delete_response.status_code == 204

    get_response = await client.get("/products/100")
    assert get_response.status_code == 404
