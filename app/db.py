import psycopg2
from fastapi import HTTPException
from psycopg2 import OperationalError
from typing import List, Optional, Dict
from datetime import datetime
from uuid import UUID
from app.models import Product
from enum import Enum

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

# Enumeração para os valores de ordenação
class SortByEnum(str, Enum):
    name = "Name"
    list_price = "ListPrice"

class SortOrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"        
    
def get_products(page: int, page_size: int, color: Optional[str], min_price: Optional[float], max_price: Optional[float], sort_by: SortByEnum, sort_order: SortOrderEnum) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * page_size
    
    sort_column = f'"Production"."Product"."{sort_by.value}"'
    sort_direction = sort_order.value

    query = f"""
        SELECT * FROM "Production"."Product"
        WHERE (%s IS NULL OR "Color" = %s)
        AND (%s IS NULL OR "ListPrice" >= %s)
        AND (%s IS NULL OR "ListPrice" <= %s)
        ORDER BY {sort_column} {sort_direction}
        LIMIT %s OFFSET %s
    """
    
    params = (
        color, color,
        min_price, min_price,
        max_price, max_price,
        page_size, offset
    )
    
    try:
        cursor.execute(query, params)
        products = cursor.fetchall()
        
        result = []
        for row in products:
            product_dict = {
                "ProductID": row[0],
                "Name": row[1],
                "ProductNumber": row[2],
                "MakeFlag": row[3],
                "FinishedGoodsFlag": row[4],
                "Color": row[5],
                "SafetyStockLevel": row[6],
                "ReorderPoint": row[7],
                "StandardCost": row[8],
                "ListPrice": row[9],
                "Size": row[10],
                "SizeUnitMeasureCode": row[11],
                "WeightUnitMeasureCode": row[12],
                "Weight": row[13],
                "DaysToManufacture": row[14],
                "ProductLine": row[15],
                "Class": row[16],
                "Style": row[17],
                "ProductSubcategoryID": row[18],
                "ProductModelID": row[19],
                "SellStartDate": row[20].isoformat() if isinstance(row[20], datetime) else row[20],  # Conversão para string
                "SellEndDate": row[21].isoformat() if isinstance(row[21], datetime) else row[21],  # Conversão para string
                "DiscontinuedDate": row[22].isoformat() if isinstance(row[22], datetime) else row[22],  # Conversão para string
                "rowguid": row[23],
                "ModifiedDate": row[24].isoformat() if isinstance(row[24], datetime) else row[24]  # Conversão para string
            }
            result.append(product_dict)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
      
    
# GET ID
def fetch_product_by_id(product_id: int) -> Optional[dict]:
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
            return None
        
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
            "rowguid": str(product[23]),
            "ModifiedDate": product[24].isoformat() if product[24] else None
        }
        
        return product_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


#Post
#@app.post("/products/", response_model=Product)
def insert_product(product: Product):
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

#Put
def update_product(product_id: int, product: Product):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
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

#Delete
def delete_product(product_id: int) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
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




