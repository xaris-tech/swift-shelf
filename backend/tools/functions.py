from typing import List, Dict, Any, Callable
from backend.services import inventory_service

FUNCTIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_inventory_overview",
            "description": "Get an overview of all products in the inventory with their current stock levels, margins, and basic metrics. Use this for general inventory questions.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_details",
            "description": "Get detailed information about a specific product including sales history. Use when asked about a specific product by ID or name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The unique identifier of the product (e.g., 'prod_001')"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_low_stock_products",
            "description": "Get products with stock below a threshold. Use when asked about low inventory, stock alerts, or products that need restocking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold": {
                        "type": "integer",
                        "description": "Stock threshold below which products are considered low (default: 10)",
                        "default": 10
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_sales_velocity",
            "description": "Get products ranked by sales velocity (units sold per day). Use when asked about best sellers, popular products, or sales trends.",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "Number of days to calculate velocity for (default: 7)",
                        "default": 7
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_high_margin_products",
            "description": "Get products with profit margin above a threshold. Use when asked about profitable products or margin analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_margin": {
                        "type": "number",
                        "description": "Minimum margin percentage (default: 30.0)",
                        "default": 30.0
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_recommendation_candidates",
            "description": "Get products that are good candidates for advertising or promotion. These are products with high margins but low visibility. Use when asked about ad recommendations, which products to promote, or marketing suggestions.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

FUNCTION_MAP: Dict[str, Callable] = {
    "get_inventory_overview": inventory_service.get_inventory_overview,
    "get_product_details": inventory_service.get_product_details,
    "get_low_stock_products": inventory_service.get_low_stock_products,
    "get_sales_velocity": inventory_service.get_sales_velocity,
    "get_high_margin_products": inventory_service.get_high_margin_products,
    "get_recommendation_candidates": inventory_service.get_recommendation_candidates,
}

def execute_function(name: str, arguments: Dict[str, Any] = None) -> Any:
    func = FUNCTION_MAP.get(name)
    if not func:
        return {"error": f"Unknown function: {name}"}
    
    if arguments is None:
        return func()
    
    return func(**{k: v for k, v in arguments.items() if v is not None})