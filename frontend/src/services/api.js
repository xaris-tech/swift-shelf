import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const queryInventory = async (query, context = null) => {
  const response = await api.post('/query', { query, context });
  return response.data;
};

export const getInventory = async () => {
  const response = await api.get('/inventory');
  return response.data;
};

export const getProduct = async (productId) => {
  const response = await api.get(`/inventory/${productId}`);
  return response.data;
};

export const getAnalyticsSummary = async () => {
  const response = await api.get('/analytics/summary');
  return response.data;
};

export const getLowStock = async (threshold = 10) => {
  const response = await api.get(`/analytics/low-stock?threshold=${threshold}`);
  return response.data;
};

export const getCriticalStock = async () => {
  const response = await api.get('/analytics/critical-stock');
  return response.data;
};

export const getSalesVelocity = async (days = 7) => {
  const response = await api.get(`/analytics/sales-velocity?days=${days}`);
  return response.data;
};

export const getHighMargin = async (minMargin = 30) => {
  const response = await api.get(`/analytics/high-margin?min_margin=${minMargin}`);
  return response.data;
};

export const getRecommendations = async () => {
  const response = await api.get('/analytics/recommendations');
  return response.data;
};

export default api;