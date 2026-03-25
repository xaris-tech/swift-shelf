from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.api.schemas import (
    QueryRequest, QueryResponse, Recommendation,
    ProductResponse, InventoryListResponse, AnalyticsSummary,
    SalesVelocityItem, ErrorResponse
)
from backend.services import inventory_service
from backend.services.llm_service import llm_service

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/query", response_model=QueryResponse)
async def query_inventory(request: QueryRequest):
    try:
        result = llm_service.process_query(request.query, request.context)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        recommendations = []
        for rec in result.get("recommendations", []):
            prod = inventory_service.get_product_by_id(rec.get("product_id", ""))
            recommendations.append(Recommendation(
                product_id=rec.get("product_id", ""),
                product_name=prod.name if prod else None,
                reason=rec.get("reason", ""),
                priority="high"
            ))
        
        return QueryResponse(
            answer=result.get("answer", ""),
            recommendations=recommendations,
            query=request.query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inventory", response_model=InventoryListResponse)
async def get_inventory():
    try:
        products = inventory_service.get_inventory_overview()
        return InventoryListResponse(products=products, total=len(products))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inventory/{product_id}")
async def get_product(product_id: str):
    product = inventory_service.get_product_details(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/analytics/summary", response_model=AnalyticsSummary)
async def get_analytics_summary():
    try:
        return inventory_service.get_analytics_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/low-stock")
async def get_low_stock(threshold: int = Query(default=10, description="Stock threshold")):
    try:
        products = inventory_service.get_low_stock_products(threshold)
        return {"products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/critical-stock")
async def get_critical_stock():
    try:
        products = inventory_service.get_critical_stock_products()
        return {"products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/sales-velocity", response_model=list)
async def get_sales_velocity(days: int = Query(default=7, ge=1, le=30)):
    try:
        return inventory_service.get_sales_velocity(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/high-margin")
async def get_high_margin(min_margin: float = Query(default=30.0, ge=0, le=100)):
    try:
        products = inventory_service.get_high_margin_products(min_margin)
        return {"products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/recommendations")
async def get_recommendations():
    try:
        candidates = inventory_service.get_recommendation_candidates()
        return {"candidates": candidates, "count": len(candidates)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))