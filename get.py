from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import psycopg2
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI()

# Definindo o modelo Product
class Product(BaseModel):
    ProductID: int
    Name: str
    ProductNumber: str
    MakeFlag: int
    FinishedGoodsFlag: int
    Color: Optional[str] = None
    SafetyStockLevel: int
    ReorderPoint: int
    StandardCost: float
    ListPrice: floatgit config  lfs.allowincompletepush true
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/", response_model=List[Product])
def get_products(
    page: int = Query(1, gt=0),  # Página inicial é 1
    page_size: int = Query(10, gt=0, le=100),  # Tamanho da página limitado a 100 produtos
    color: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query('Name', enum=['Name', 'ListPrice']),
    sort_order: Optional[str] = Query('asc', enum=['asc', 'desc'])
):
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * page_size
    
    # Garantir que o nome da coluna está qualificado corretamente
    valid_sort_by = sort_by if sort_by in ['Name', 'ListPrice'] else 'Name'
    sort_column = f'"Production"."Product"."{valid_sort_by}"'
    query = f"""
        SELECT * FROM "Production"."Product"
        WHERE (%s IS NULL OR "Color" = %s)
        AND (%s IS NULL OR "ListPrice" >= %s)
        AND (%s IS NULL OR "ListPrice" <= %s)
        ORDER BY {sort_column} {sort_order}
        LIMIT %s OFFSET %s
    """
    
    # Montar a tupla de parâmetros
    params = (
        color, color,
        min_price, min_price,
        max_price, max_price,
        page_size, offset
    )
    
    cursor.execute(query, params)
    products = cursor.fetchall()
    
    # Convertendo os resultados para o formato esperado pelo Pydantic
    result = []
    for row in products:
        product = Product(
            ProductID=row[0],
            Name=row[1],
            ProductNumber=row[2],
            MakeFlag=row[3],
            FinishedGoodsFlag=row[4],
            Color=row[5],
            SafetyStockLevel=row[6],
            ReorderPoint=row[7],
            StandardCost=row[8],
            ListPrice=row[9],
            Size=row[10],
            SizeUnitMeasureCode=row[11],
            WeightUnitMeasureCode=row[12],
            Weight=row[13],
            DaysToManufacture=row[14],
            ProductLine=row[15],
            Class=row[16],
            Style=row[17],
            ProductSubcategoryID=row[18],
            ProductModelID=row[19],
            SellStartDate=row[20],
            SellEndDate=row[21],
            DiscontinuedDate=row[22],
            rowguid=row[23],
            ModifiedDate=row[24]
        )
        result.append(product)
    
    cursor.close()
    conn.close()
    
    return result
