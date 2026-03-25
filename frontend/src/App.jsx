import { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import InventoryTab from './components/InventoryTab';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-brand">
          <svg className="brand-icon" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
          </svg>
          <span className="brand-name">SwiftShelf</span>
        </div>
        <nav className="nav">
          <button 
            className={activeTab === 'dashboard' ? 'active' : ''} 
            onClick={() => setActiveTab('dashboard')}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
              <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
            </svg>
            Dashboard
          </button>
          <button 
            className={activeTab === 'inventory' ? 'active' : ''} 
            onClick={() => setActiveTab('inventory')}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
            </svg>
            Inventory
          </button>
        </nav>
      </header>

      <main className="app-main">
        {activeTab === 'dashboard' && (
          <div className="dashboard-split">
            <div className="dashboard-panel">
              <ChatInterface />
            </div>
            <div className="dashboard-panel">
              <AnalyticsDashboard />
            </div>
          </div>
        )}
        
        {activeTab === 'inventory' && (
          <InventoryTab />
        )}
      </main>

      <footer className="app-footer">
        <p>SwiftShelf • Powered by OpenRouter AI</p>
      </footer>
    </div>
  );
}

export default App;