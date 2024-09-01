
import pytest
import httpx
import subprocess
import time
from app.main import app
from app.models import Product
from app.db import fetch_product_by_id

def test_fetch_product_by_id():
    product = fetch_product_by_id(1)
    assert product is not None
    assert product["ProductID"] == 1
    assert product["Name"] == "Adjustable Race"