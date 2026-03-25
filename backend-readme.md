# Smart Stock Manager - Backend

AI-Driven Inventory & Trend Predictor using FastAPI and OpenRouter.

## Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure API key**:
Edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Get a free key at: https://openrouter.ai/

## Run

```bash
cd src
python main.py
```

Server runs at: http://localhost:8000
API Docs: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/query` | Natural language query |
| GET | `/api/inventory` | All products |
| GET | `/api/inventory/{id}` | Single product |
| GET | `/api/analytics/summary` | Inventory summary |
| GET | `/api/analytics/low-stock` | Low stock items |
| GET | `/api/analytics/critical-stock` | Critical stock |
| GET | `/api/analytics/sales-velocity` | Sales ranking |
| GET | `/api/analytics/high-margin` | High margin products |
| GET | `/api/analytics/recommendations` | Ad recommendations |

## Example Queries

- "Which products should I run ads for this week?"
- "What needs restocking?"
- "What's selling well?"
- "Which products have the best margin?"
- "Give me an overview of inventory"