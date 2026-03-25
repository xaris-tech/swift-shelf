from datetime import datetime, timedelta
from typing import List
import random

class SaleRecord:
    def __init__(self, date: str, quantity: int):
        self.date = date
        self.quantity = quantity

class Product:
    def __init__(
        self,
        id: str,
        name: str,
        category: str,
        cost: float,
        price: float,
        stock: int,
        visibility_score: int,
        ad_spend: float,
        sales_history: List[dict],
        image_url: str = ""
    ):
        self.id = id
        self.name = name
        self.category = category
        self.cost = cost
        self.price = price
        self.stock = stock
        self.visibility_score = visibility_score
        self.ad_spend = ad_spend
        self.sales_history = [SaleRecord(**record) for record in sales_history]
        self.image_url = image_url

    @property
    def margin_percent(self) -> float:
        return round(((self.price - self.cost) / self.price) * 100, 2)

    @property
    def stock_status(self) -> str:
        if self.stock < 5:
            return "critical"
        elif self.stock < 20:
            return "low"
        return "healthy"

    def get_sales_velocity(self, days: int = 7) -> float:
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        total = sum(s.quantity for s in self.sales_history if s.date >= cutoff)
        return round(total / days, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "cost": self.cost,
            "price": self.price,
            "stock": self.stock,
            "visibility_score": self.visibility_score,
            "ad_spend": self.ad_spend,
            "margin_percent": self.margin_percent,
            "stock_status": self.stock_status,
            "sales_velocity_7d": self.get_sales_velocity(7),
            "sales_velocity_30d": self.get_sales_velocity(30),
            "image_url": self.image_url
        }

def generate_sales_history(base_daily: int, variance: float = 0.5) -> List[dict]:
    history = []
    today = datetime.now()
    for i in range(30):
        date = (today - timedelta(days=29-i)).strftime("%Y-%m-%d")
        quantity = max(0, int(base_daily * random.uniform(1-variance, 1+variance)))
        history.append({"date": date, "quantity": quantity})
    return history

def get_mock_products() -> List[Product]:
    return [
        Product(
            id="prod_001",
            name="Wireless Earbuds Pro",
            category="Electronics",
            cost=30.00,
            price=79.99,
            stock=45,
            visibility_score=85,
            ad_spend=50.00,
            sales_history=generate_sales_history(8),
            image_url="/images/wireless-budspro.jpg"
        ),
        Product(
            id="prod_002",
            name="Smart Watch Series 5",
            category="Electronics",
            cost=80.00,
            price=199.99,
            stock=12,
            visibility_score=90,
            ad_spend=75.00,
            sales_history=generate_sales_history(5),
            image_url="/images/Smart Watch Series 5.jpg"
        ),
        Product(
            id="prod_003",
            name="Portable Charger 20000mAh",
            category="Electronics",
            cost=15.00,
            price=39.99,
            stock=150,
            visibility_score=20,
            ad_spend=10.00,
            sales_history=generate_sales_history(12),
            image_url="/images/Portable Charger 20000mAh.jpg"
        ),
        Product(
            id="prod_004",
            name="Indoor Plant Pot Set",
            category="Home & Garden",
            cost=12.00,
            price=34.99,
            stock=8,
            visibility_score=60,
            ad_spend=15.00,
            sales_history=generate_sales_history(3),
            image_url="https://picsum.photos/seed/plants/400/300"
        ),
        Product(
            id="prod_005",
            name="LED Desk Lamp",
            category="Home & Garden",
            cost=18.00,
            price=49.99,
            stock=65,
            visibility_score=35,
            ad_spend=20.00,
            sales_history=generate_sales_history(6),
            image_url="https://picsum.photos/seed/lamp/400/300"
        ),
        Product(
            id="prod_006",
            name="Memory Foam Pillow",
            category="Home & Garden",
            cost=8.00,
            price=29.99,
            stock=200,
            visibility_score=15,
            ad_spend=5.00,
            sales_history=generate_sales_history(15),
            image_url="https://picsum.photos/seed/pillow/400/300"
        ),
        Product(
            id="prod_007",
            name="Running Shoes Elite",
            category="Fashion",
            cost=35.00,
            price=89.99,
            stock=30,
            visibility_score=75,
            ad_spend=40.00,
            sales_history=generate_sales_history(7),
            image_url="https://picsum.photos/seed/shoes/400/300"
        ),
        Product(
            id="prod_008",
            name="Denim Jacket Classic",
            category="Fashion",
            cost=25.00,
            price=69.99,
            stock=5,
            visibility_score=40,
            ad_spend=25.00,
            sales_history=generate_sales_history(2),
            image_url="https://picsum.photos/seed/jacket/400/300"
        ),
        Product(
            id="prod_009",
            name="Canvas Backpack",
            category="Fashion",
            cost=15.00,
            price=45.99,
            stock=90,
            visibility_score=25,
            ad_spend=12.00,
            sales_history=generate_sales_history(9),
            image_url="https://picsum.photos/seed/backpack/400/300"
        ),
        Product(
            id="prod_010",
            name="Yoga Mat Premium",
            category="Sports",
            cost=10.00,
            price=34.99,
            stock=120,
            visibility_score=30,
            ad_spend=15.00,
            sales_history=generate_sales_history(10),
            image_url="https://picsum.photos/seed/yogamat/400/300"
        ),
        Product(
            id="prod_011",
            name="Adjustable Dumbbells",
            category="Sports",
            cost=40.00,
            price=99.99,
            stock=8,
            visibility_score=55,
            ad_spend=30.00,
            sales_history=generate_sales_history(4),
            image_url="https://picsum.photos/seed/dumbbells/400/300"
        ),
        Product(
            id="prod_012",
            name="Fitness Tracker Band",
            category="Sports",
            cost=20.00,
            price=49.99,
            stock=75,
            visibility_score=45,
            ad_spend=20.00,
            sales_history=generate_sales_history(11),
            image_url="https://picsum.photos/seed/fitnessband/400/300"
        ),
    ]

MOCK_PRODUCTS = get_mock_products()

def get_all_products() -> List[Product]:
    return MOCK_PRODUCTS

def get_product_by_id(product_id: str) -> Product | None:
    for product in MOCK_PRODUCTS:
        if product.id == product_id:
            return product
    return None