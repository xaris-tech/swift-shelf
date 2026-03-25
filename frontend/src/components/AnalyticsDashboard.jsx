import { useState, useEffect } from 'react';
import { getAnalyticsSummary, getLowStock, getSalesVelocity, getRecommendations } from '../services/api';
import './AnalyticsDashboard.css';

function AnalyticsDashboard() {
  const [summary, setSummary] = useState(null);
  const [lowStock, setLowStock] = useState([]);
  const [velocity, setVelocity] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('summary');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [summaryData, lowStockData, velocityData, recData] = await Promise.all([
        getAnalyticsSummary(),
        getLowStock(20),
        getSalesVelocity(7),
        getRecommendations()
      ]);
      setSummary(summaryData);
      setLowStock(lowStockData.products);
      setVelocity(velocityData);
      setRecommendations(recData.candidates);
    } catch (err) {
      console.error('Failed to load analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="dashboard-loading">Loading analytics...</div>;
  }

  return (
    <div className="analytics-dashboard">
      <div className="dashboard-header">
        <div className="header-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 3v18h18"/>
            <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/>
          </svg>
        </div>
        <h2>SwiftShelf Analytics</h2>
      </div>

      <div className="tabs">
        <button className={activeTab === 'summary' ? 'active' : ''} onClick={() => setActiveTab('summary')}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
          </svg>
          Overview
        </button>
        <button className={activeTab === 'velocity' ? 'active' : ''} onClick={() => setActiveTab('velocity')}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
            <polyline points="17 6 23 6 23 12"/>
          </svg>
          Sales Velocity
        </button>
        <button className={activeTab === 'lowstock' ? 'active' : ''} onClick={() => setActiveTab('lowstock')}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
          Low Stock
        </button>
        <button className={activeTab === 'recommendations' ? 'active' : ''} onClick={() => setActiveTab('recommendations')}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/>
            <line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/>
          </svg>
          Ad Recommendations
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'summary' && summary && (
          <div className="summary-grid">
            <div className="stat-card">
              <div className="stat-value">{summary.total_products}</div>
              <div className="stat-label">Total Products</div>
            </div>
            <div className="stat-card warning">
              <div className="stat-value">{summary.low_stock_count}</div>
              <div className="stat-label">Low Stock</div>
            </div>
            <div className="stat-card danger">
              <div className="stat-value">{summary.critical_stock_count}</div>
              <div className="stat-label">Critical Stock</div>
            </div>
            <div className="stat-card success">
              <div className="stat-value">{summary.average_margin_percent}%</div>
              <div className="stat-label">Avg Margin</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">${summary.total_inventory_value.toLocaleString()}</div>
              <div className="stat-label">Inventory Value</div>
            </div>
          </div>
        )}

        {activeTab === 'velocity' && (
          <div className="velocity-list">
            <h3>Top Selling Products (7-day velocity)</h3>
            {velocity.map((item, idx) => (
              <div key={item.id} className="velocity-item">
                <span className="rank">#{idx + 1}</span>
                <span className="name">{item.name}</span>
                <span className="category">{item.category}</span>
                <span className="velocity">{item.sales_velocity} units/day</span>
                <span className={`stock ${item.stock < 20 ? 'low' : ''}`}>{item.stock} in stock</span>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'lowstock' && (
          <div className="low-stock-list">
            <h3>Products Needing Restock</h3>
            {lowStock.length === 0 ? (
              <p className="no-data">All products are well-stocked!</p>
            ) : (
              lowStock.map(item => (
                <div key={item.id} className={`stock-item ${item.stock_status}`}>
                  <div className="item-info">
                    <span className="name">{item.name}</span>
                    <span className="category">{item.category}</span>
                  </div>
                  <div className="item-stock">
                    <span className="stock-value">{item.stock}</span>
                    <span className="stock-label">units</span>
                    <span className={`status ${item.stock_status}`}>{item.stock_status}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div className="recommendations-list">
            <h3>Products Ready for Advertising</h3>
            {recommendations.length === 0 ? (
              <p className="no-data">No products meet the criteria for ad recommendations.</p>
            ) : (
              recommendations.map(item => (
                <div key={item.id} className="rec-item">
                  <div className="rec-info">
                    <span className="name">{item.name}</span>
                    <span className="category">{item.category}</span>
                  </div>
                  <div className="rec-metrics">
                    <div className="metric">
                      <span className="value">{item.margin_percent}%</span>
                      <span className="label">margin</span>
                    </div>
                    <div className="metric">
                      <span className="value">{item.visibility_score}</span>
                      <span className="label">visibility</span>
                    </div>
                    <div className="metric">
                      <span className="value">{item.stock}</span>
                      <span className="label">stock</span>
                    </div>
                  </div>
                  <div className="rec-score">
                    <span className="score-value">{item.recommendation_score}</span>
                    <span className="score-label">score</span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default AnalyticsDashboard;