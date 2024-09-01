from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import OperationalError
from typing import List, Dict, Optional
from pydantic import BaseModel, validator
from uuid import UUID

app = FastAPI()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="My_password1"
        )
        return conn
    except OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Definindo o modelo Pydantic para produtos
class Product(BaseModel):
    ProductID: int
    Name: str
    ProductNumber: str
    MakeFlag: int
    FinishedGoodsFlag: int
    Color: Optional[str]
    SafetyStockLevel: int
    ReorderPoint: int
    StandardCost: float
    ListPrice: float
    Size: Optional[str]
    SizeUnitMeasureCode: Optional[str]
    WeightUnitMeasureCode: Optional[str]
    Weight: Optional[float]
    DaysToManufacture: int
    ProductLine: Optional[str]
    Class: Optional[str]
    Style: Optional[str]
    ProductSubcategoryID: Optional[int]
    ProductModelID: Optional[int]
    SellStartDate: str
    SellEndDate: Optional[str]
    DiscontinuedDate: Optional[str]
    rowguid: UUID
    ModifiedDate: str        

@app.get("/products/")
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Ajuste a consulta para usar o esquema correto e garantir a capitalização correta
        cursor.execute('SELECT * FROM "Production"."Product"')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        products = [dict(zip(columns, row)) for row in rows]
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/products/", response_model=Product)
def create_product(product: Product):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO "Production"."Product" (
                "ProductID", "Name", "ProductNumber", "MakeFlag", "FinishedGoodsFlag", "Color", 
                "SafetyStockLevel", "ReorderPoint", "StandardCost", "ListPrice", "Size", 
                "SizeUnitMeasureCode", "WeightUnitMeasureCode", "Weight", "DaysToManufacture", 
                "ProductLine", "Class", "Style", "ProductSubcategoryID", "ProductModelID", 
                "SellStartDate", "SellEndDate", "DiscontinuedDate", "rowguid", "ModifiedDate"
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            product.ProductID, 
            product.Name, 
            product.ProductNumber, 
            product.MakeFlag, 
            product.FinishedGoodsFlag, 
            product.Color, 
            product.SafetyStockLevel, 
            product.ReorderPoint, 
            product.StandardCost, 
            product.ListPrice, 
            product.Size, 
            product.SizeUnitMeasureCode, 
            product.WeightUnitMeasureCode, 
            product.Weight, 
            product.DaysToManufacture, 
            product.ProductLine, 
            product.Class, 
            product.Style, 
            product.ProductSubcategoryID, 
            product.ProductModelID, 
            product.SellStartDate, 
            product.SellEndDate, 
            product.DiscontinuedDate, 
            str(product.rowguid),  
            product.ModifiedDate
        ))
        conn.commit()
        return product
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT "ProductID", "Name", "ProductNumber", "MakeFlag", "FinishedGoodsFlag", "Color", 
                   "SafetyStockLevel", "ReorderPoint", "StandardCost", "ListPrice", "Size", 
                   "SizeUnitMeasureCode", "WeightUnitMeasureCode", "Weight", "DaysToManufacture", 
                   "ProductLine", "Class", "Style", "ProductSubcategoryID", "ProductModelID", 
                   "SellStartDate", "SellEndDate", "DiscontinuedDate", "rowguid", "ModifiedDate"
            FROM "Production"."Product"
            WHERE "ProductID" = %s
        """, (product_id,))
        
        product = cursor.fetchone()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Convert the fetched data to a dictionary with date formatting
        product_dict = {
            "ProductID": product[0],
            "Name": product[1],
            "ProductNumber": product[2],
            "MakeFlag": product[3],
            "FinishedGoodsFlag": product[4],
            "Color": product[5],
            "SafetyStockLevel": product[6],
            "ReorderPoint": product[7],
            "StandardCost": product[8],
            "ListPrice": product[9],
            "Size": product[10],
            "SizeUnitMeasureCode": product[11],
            "WeightUnitMeasureCode": product[12],
            "Weight": product[13],
            "DaysToManufacture": product[14],
            "ProductLine": product[15],
            "Class": product[16],
            "Style": product[17],
            "ProductSubcategoryID": product[18],
            "ProductModelID": product[19],
            "SellStartDate": product[20].isoformat() if product[20] else None,
            "SellEndDate": product[21].isoformat() if product[21] else None,
            "DiscontinuedDate": product[22].isoformat() if product[22] else None,
            "rowguid": str(product[23]),  # Convert UUID to string
            "ModifiedDate": product[24].isoformat() if product[24] else None
        }
        
        return product_dict
    except Exception as e:
        # Log the exception details
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Executar o comando de atualização
        cursor.execute("""
            UPDATE "Production"."Product"
            SET 
                "Name" = %s, 
                "ProductNumber" = %s, 
                "MakeFlag" = %s, 
                "FinishedGoodsFlag" = %s, 
                "Color" = %s, 
                "SafetyStockLevel" = %s, 
                "ReorderPoint" = %s, 
                "StandardCost" = %s, 
                "ListPrice" = %s, 
                "Size" = %s, 
                "SizeUnitMeasureCode" = %s, 
                "WeightUnitMeasureCode" = %s, 
                "Weight" = %s, 
                "DaysToManufacture" = %s, 
                "ProductLine" = %s, 
                "Class" = %s, 
                "Style" = %s, 
                "ProductSubcategoryID" = %s, 
                "ProductModelID" = %s, 
                "SellStartDate" = %s, 
                "SellEndDate" = %s, 
                "DiscontinuedDate" = %s, 
                "rowguid" = %s, 
                "ModifiedDate" = %s
            WHERE "ProductID" = %s
        """, (
            product.Name, 
            product.ProductNumber, 
            product.MakeFlag, 
            product.FinishedGoodsFlag, 
            product.Color, 
            product.SafetyStockLevel, 
            product.ReorderPoint, 
            product.StandardCost, 
            product.ListPrice, 
            product.Size, 
            product.SizeUnitMeasureCode, 
            product.WeightUnitMeasureCode, 
            product.Weight, 
            product.DaysToManufacture, 
            product.ProductLine, 
            product.Class, 
            product.Style, 
            product.ProductSubcategoryID, 
            product.ProductModelID, 
            product.SellStartDate, 
            product.SellEndDate, 
            product.DiscontinuedDate, 
            str(product.rowguid),  
            product.ModifiedDate,
            product_id
        ))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Executar o comando de exclusão
        cursor.execute("""
            DELETE FROM "Production"."Product"
            WHERE "ProductID" = %s
        """, (product_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@validator('StandardCost', 'ListPrice', pre=True, always=True)
def check_positive(cls, v):
    if v < 0:
        raise ValueError('Must be a positive number')
    return v