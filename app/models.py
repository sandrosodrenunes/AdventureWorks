from pydantic import BaseModel, validator
from typing import Optional
from uuid import UUID
import uuid

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
    rowguid: uuid.UUID
    ModifiedDate: str
    
    @validator('StandardCost', 'ListPrice', pre=True, always=True)
    def check_positive(cls, v):
        if v < 0:
            raise ValueError('Must be a positive number')
        return v