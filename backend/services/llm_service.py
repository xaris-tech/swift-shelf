import os
import json
from typing import List, Dict, Any, Optional
import httpx
from dotenv import load_dotenv
from backend.tools.functions import FUNCTIONS, execute_function

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

SYSTEM_PROMPT = """You are SwiftShelf, an AI assistant for e-commerce inventory management.

You have access to the following tools to query inventory data:
- get_inventory_overview: Get all products with stock levels and metrics
- get_product_details: Get details for a specific product by ID
- get_low_stock_products: Get products with low inventory
- get_sales_velocity: Get products ranked by sales speed
- get_high_margin_products: Get products with high profit margins
- get_recommendation_candidates: Get products good for advertising (high margin + low visibility)

When user asks questions:
1. Use relevant tools to get the data
2. Analyze the data
3. Provide clear, actionable insights

Always be specific with numbers and percentages. If data is insufficient, explain what you need.

Example questions you can answer:
- "Which products should I run ads for?"
- "What needs restocking?"
- "What's selling well?"
- "Which products have the best margin?"
- "Give me an overview of inventory"

Format your response with clear sections when needed."""


class LLMService:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self.model = OPENROUTER_MODEL
        self.base_url = "https://openrouter.ai/api/v1"
    
    def _call_api(self, messages: List[Dict[str, Any]], tools: List[Dict] = None) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "SwiftShelf"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        
        if tools:
            payload["tools"] = tools
        
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    def process_query(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        user_message = query
        if context:
            user_message = f"{context}\n\nUser question: {query}"
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
        
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            response = self._call_api(messages, FUNCTIONS)
            choices = response.get("choices", [])
            if not choices:
                return {"error": "No response from LLM", "raw": response}
            
            message = choices[0].get("message", {})
            content = message.get("content", "")
            tool_calls = message.get("tool_calls", [])
            
            if content:
                messages.append({"role": "assistant", "content": content})
            
            if not tool_calls:
                break
            
            for tool_call in tool_calls:
                func_name = tool_call.get("function", {}).get("name")
                func_args = json.loads(tool_call.get("function", {}).get("arguments", "{}"))
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.get("id"),
                    "content": json.dumps(execute_function(func_name, func_args))
                })
            
            if iteration == max_iterations:
                return {
                    "error": "Maximum iterations reached",
                    "partial_response": content if content else "Function calls did not complete"
                }
        
        final_message = message.get("content", "")
        
        recommendations = self._extract_recommendations(content) if content else []
        
        return {
            "answer": final_message,
            "recommendations": recommendations
        }
    
    def _extract_recommendations(self, content: str) -> List[Dict[str, Any]]:
        recommendations = []
        
        lines = content.split("\n")
        for line in lines:
            if any(marker in line.lower() for marker in ["prod_", "id:", "product:"]):
                parts = line.split()
                for part in parts:
                    if part.startswith("prod_"):
                        recommendations.append({
                            "product_id": part.strip(":,)"),
                            "reason": line
                        })
                        break
        
        return recommendations[:5]

llm_service = LLMService()