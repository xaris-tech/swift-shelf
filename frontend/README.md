# CompareCart Frontend

AI-Driven Inventory & Trend Predictor - React Frontend

## Setup

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Start development server**:
```bash
npm run dev
```

3. **Build for production**:
```bash
npm run build
```

## Features

### AI Assistant (Chat Interface)
- Natural language queries to inventory data
- Uses LLM function calling to analyze inventory
- Pre-defined suggestion buttons for common queries
- Displays recommendations with product details

### Analytics Dashboard
- **Overview**: Summary cards showing total products, low/critical stock, avg margin, inventory value
- **Sales Velocity**: Products ranked by units sold per day
- **Low Stock**: Products needing restocking with status indicators
- **Ad Recommendations**: Products with high margin but low visibility ready for advertising

## API Connection

The frontend connects to the FastAPI backend at `http://localhost:8000/api`.

Make sure the backend is running first:
```bash
cd src
python main.py
```

## Navigation

- **AI Assistant**: Main chat interface for natural language queries
- **Analytics**: Dashboard with inventory metrics and recommendations