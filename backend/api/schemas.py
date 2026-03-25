from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query about inventory")
    context: Optional[str] = Field(None, description="Optional context for the query")

class Recommendation(BaseModel):
    product_id: str
    product_name: Optional[str] = None
    reason: str
    priority: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    recommendations: List[Recommendation] = []
    query: str

class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    cost: float
    price: float
    stock: int
    visibility_score: int
    ad_spend: float
    margin_percent: float
    stock_status: str
    sales_velocity_7d: float
    sales_velocity_30d: float

class InventoryListResponse(BaseModel):
    products: List[ProductResponse]
    total: int

class AnalyticsSummary(BaseModel):
    total_products: int
    low_stock_count: int
    critical_stock_count: int
    average_margin_percent: float
    total_inventory_value: float
    categories: List[str]

class SalesVelocityItem(BaseModel):
    id: str
    name: str
    category: str
    sales_velocity: float
    stock: int

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None