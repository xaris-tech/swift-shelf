import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { queryInventory } from '../services/api';
import './ChatInterface.css';

const SUGGESTED_QUERIES = [
  "Which products should I run ads for?",
  "What needs restocking?",
  "What's selling well this week?",
  "Show me high margin products",
];

const THINKING_STEPS = [
  "Analyzing your query...",
  "Fetching inventory data...",
  "Calculating metrics...",
  "Generating insights...",
];

function ChatInterface() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! I\'m SwiftShelf. Ask me about your inventory, and I\'ll analyze the data to give you actionable insights. Try: "Which products should I run ads for?"' }
  ]);
  const [loading, setLoading] = useState(false);
  const [thinkingStep, setThinkingStep] = useState('');
  const [thinkingIndex, setThinkingIndex] = useState(0);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userQuery = query.trim();
    setQuery('');
    setError(null);

    setMessages(prev => [...prev, { role: 'user', content: userQuery }]);
    setLoading(true);
    setThinkingIndex(0);

    const thinkingInterval = setInterval(() => {
      setThinkingIndex(prev => {
        if (prev < THINKING_STEPS.length - 1) {
          setThinkingStep(THINKING_STEPS[prev + 1]);
          return prev + 1;
        }
        return prev;
      });
    }, 800);

    try {
      const response = await queryInventory(userQuery);
      clearInterval(thinkingInterval);
      setThinkingStep('');
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: response.answer,
          recommendations: response.recommendations
        }
      ]);
    } catch (err) {
      clearInterval(thinkingInterval);
      setThinkingStep('');
      setError(err.response?.data?.detail || err.message || 'Failed to get response');
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestion = (suggestion) => {
    setQuery(suggestion);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
        <h2>SwiftShelf Assistant</h2>
        <p>Ask questions about your inventory in plain English</p>
      </div>

      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-content">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
              {msg.recommendations && msg.recommendations.length > 0 && (
                <div className="recommendations">
                  <h4>Recommendations:</h4>
                  <ul>
                    {msg.recommendations.map((rec, recIdx) => (
                      <li key={recIdx}>
                        <strong>{rec.product_name || rec.product_id}</strong>: {rec.reason}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="message-content loading">
              <div className="thinking-animation">
                <div className="thinking-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <div className="thinking-text">
                  <span className="thinking-step">{thinkingStep || THINKING_STEPS[0]}</span>
                </div>
              </div>
            </div>
          </div>
        )}
        {error && (
          <div className="message error">
            <div className="message-content">{error}</div>
          </div>
        )}
      </div>

      <div className="suggestions">
        {SUGGESTED_QUERIES.map((sq, idx) => (
          <button key={idx} onClick={() => handleSuggestion(sq)} disabled={loading}>
            {sq}
          </button>
        ))}
      </div>

      <form className="chat-input" onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about your inventory..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !query.trim()}>
          {loading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;