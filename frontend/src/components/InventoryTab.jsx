import { useState, useEffect } from 'react';
import { getInventory } from '../services/api';
import './InventoryTab.css';

function InventoryTab() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const data = await getInventory();
      setProducts(data.products);
    } catch (err) {
      console.error('Failed to load inventory:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredProducts = products.filter(p => 
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.category.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return <div className="inventory-loading">Loading inventory...</div>;
  }

  return (
    <div className="inventory-tab">
      <div className="inventory-header">
        <div className="search-box">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            type="text"
            placeholder="Search products..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="products-grid">
        {filteredProducts.map(product => (
          <div key={product.id} className="product-card">
            <div className="product-image">
              <img 
                src={product.image_url || `https://placehold.co/400x300/e9ecef/0d6efd?text=${encodeURIComponent(product.name.split(' ')[0])}`}
                alt={product.name}
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = `https://via.placeholder.com/400x300/0d6efd/ffffff?text=${encodeURIComponent(product.name.split(' ')[0])}`;
                }}
              />
              <span className={`stock-badge ${product.stock_status}`}>
                {product.stock_status}
              </span>
            </div>
            <div className="product-info">
              <h3>{product.name}</h3>
              <span className="category">{product.category}</span>
              <div className="product-details">
                <div className="detail">
                  <span className="label">Price</span>
                  <span className="value">${product.price.toFixed(2)}</span>
                </div>
                <div className="detail">
                  <span className="label">Cost</span>
                  <span className="value">${product.cost.toFixed(2)}</span>
                </div>
                <div className="detail">
                  <span className="label">Margin</span>
                  <span className="value">{product.margin_percent}%</span>
                </div>
              </div>
              <div className="stock-row">
                <span className="stock-label">Stock:</span>
                <span className={`stock-value ${product.stock_status}`}>{product.stock} units</span>
              </div>
              <div className="velocity-row">
                <span className="velocity-label">Sales (7d):</span>
                <span className="velocity-value">{product.sales_velocity_7d}/day</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default InventoryTab;