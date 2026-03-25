from typing import List, Dict, Any
from backend.data.mock_db import get_all_products, get_product_by_id

def get_inventory_overview() -> List[Dict[str, Any]]:
    products = get_all_products()
    return [p.to_dict() for p in products]

def get_product_details(product_id: str) -> Dict[str, Any] | None:
    product = get_product_by_id(product_id)
    if product:
        return {
            **product.to_dict(),
            "sales_history": [{"date": s.date, "quantity": s.quantity} for s in product.sales_history]
        }
    return None

def get_low_stock_products(threshold: int = 10) -> List[Dict[str, Any]]:
    products = get_all_products()
    return [p.to_dict() for p in products if p.stock < threshold]

def get_sales_velocity(days: int = 7) -> List[Dict[str, Any]]:
    products = get_all_products()
    sorted_products = sorted(products, key=lambda p: p.get_sales_velocity(days), reverse=True)
    return [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "sales_velocity": p.get_sales_velocity(days),
            "stock": p.stock
        }
        for p in sorted_products
    ]

def get_high_margin_products(min_margin: float = 30.0) -> List[Dict[str, Any]]:
    products = get_all_products()
    return [p.to_dict() for p in products if p.margin_percent >= min_margin]

def get_recommendation_candidates() -> List[Dict[str, Any]]:
    products = get_all_products()
    candidates = []
    
    for p in products:
        if p.margin_percent >= 30 and p.visibility_score <= 40 and p.stock >= 20:
            score = (
                p.margin_percent * 0.4 +
                (100 - p.visibility_score) * 0.3 +
                p.get_sales_velocity(7) * 10 * 0.3
            )
            candidates.append({
                **p.to_dict(),
                "recommendation_score": round(score, 2)
            })
    
    return sorted(candidates, key=lambda x: x["recommendation_score"], reverse=True)

def get_products_by_category(category: str) -> List[Dict[str, Any]]:
    products = get_all_products()
    return [p.to_dict() for p in products if p.category.lower() == category.lower()]

def get_critical_stock_products() -> List[Dict[str, Any]]:
    products = get_all_products()
    return [p.to_dict() for p in products if p.stock_status == "critical"]

def get_analytics_summary() -> Dict[str, Any]:
    products = get_all_products()
    total_products = len(products)
    low_stock = sum(1 for p in products if p.stock_status in ["low", "critical"])
    critical = sum(1 for p in products if p.stock_status == "critical")
    avg_margin = sum(p.margin_percent for p in products) / total_products
    total_value = sum(p.price * p.stock for p in products)
    
    return {
        "total_products": total_products,
        "low_stock_count": low_stock,
        "critical_stock_count": critical,
        "average_margin_percent": round(avg_margin, 2),
        "total_inventory_value": round(total_value, 2),
        "categories": list(set(p.category for p in products))
    }