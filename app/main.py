from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import psycopg2
from typing import List, Optional, Dict
from datetime import datetime
import uuid
from app.models import Product
from app.db import fetch_product_by_id, insert_product, update_product, delete_product, get_products

app = FastAPI()

# GET Filtragem e Ordenação
@app.get("/products/", response_model=List[Product])
def get_products_endpoint(
    page: int = Query(1, gt=0),  
    page_size: int = Query(10, gt=0, le=100), 
    color: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query('Name', enum=['Name', 'ListPrice']),
    sort_order: Optional[str] = Query('asc', enum=['asc', 'desc'])
):
    products = get_products(
        page=page,
        page_size=page_size,
        color=color,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return products

# GET ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = fetch_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# POST
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    try:
        created_product = insert_product(product)
        return created_product
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
#Put
@app.put("/products/{product_id}", response_model=Product)
def update_product_endpoint(product_id: int, product: Product):
    try:
        updated_product = update_product(product_id, product)
        return updated_product
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

#Delete
@app.delete("/products/{product_id}", status_code=204)
def delete_product_endpoint(product_id: int):
    try:
        delete_product(product_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

# @app.get("/products/")
# def get_products():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     try:
#         # Ajuste a consulta para usar o esquema correto e garantir a capitalização correta
#         cursor.execute('SELECT * FROM "Production"."Product"')
#         rows = cursor.fetchall()
#         columns = [desc[0] for desc in cursor.description]
#         products = [dict(zip(columns, row)) for row in rows]
#         return products
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         cursor.close()
#         conn.close()

