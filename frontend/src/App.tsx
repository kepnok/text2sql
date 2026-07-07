import React, { useState } from 'react';
import axios from 'axios';
import { Database, Terminal, Play, AlertCircle } from 'lucide-react';

interface QueryResponse {
  sql: string;
  results?: any[];
  error?: string;
}

const API_URL = 'http://localhost:8000/api';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResponse(null);

    try {
      const res = await axios.post<QueryResponse>(`${API_URL}/generate-sql`, { query });
      setResponse(res.data);
    } catch (err: any) {
      setResponse({
        sql: '',
        error: err.message || 'An error occurred while communicating with the server.',
      });
    } finally {
      setLoading(false);
    }
  };

  // Simple SQL highlighting
  const highlightSql = (sql: string) => {
    const keywords = ['SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'ORDER BY', 'GROUP BY', 'LIMIT', 'JOIN', 'ON', 'AS', 'IN', 'IS', 'NULL'];
    let highlighted = sql;
    keywords.forEach(kw => {
      const regex = new RegExp(`\\b${kw}\\b`, 'gi');
      highlighted = highlighted.replace(regex, `<span class="keyword">$&</span>`);
    });
    return { __html: highlighted };
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Text2SQL AI</h1>
        <p>Ask your database questions in natural language.</p>
      </header>

      <div className="glass-panel">
        <form className="search-section" onSubmit={handleSubmit}>
          <input
            type="text"
            className="search-input"
            placeholder="E.g., Show me all employees in the Engineering department with salary over 70000"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />
          <button type="submit" className="submit-btn" disabled={loading || !query.trim()}>
            {loading ? <div className="loader" /> : <><Play size={18} /> Run Query</>}
          </button>
        </form>

        {response?.error && (
          <div className="error-message flex items-center gap-2">
            <AlertCircle size={20} />
            {response.error}
          </div>
        )}

        {response?.sql && !response.error && (
          <div className="sql-viewer">
            <h3><Terminal size={20} /> Generated SQL</h3>
            <div className="code-block" dangerouslySetInnerHTML={highlightSql(response.sql)} />
          </div>
        )}

        {response?.results && response.results.length > 0 && (
          <div className="results-section">
            <h3><Database size={20} className="inline-block mr-2" /> Results</h3>
            <div style={{ overflowX: 'auto', marginTop: '1rem', border: '1px solid var(--border-color)', borderRadius: '8px' }}>
              <table>
                <thead>
                  <tr>
                    {Object.keys(response.results[0]).map((key) => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {response.results.map((row, i) => (
                    <tr key={i}>
                      {Object.values(row).map((val: any, j) => (
                        <td key={j}>{val?.toString()}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
        
        {response?.results && response.results.length === 0 && (
          <div className="mt-4 p-4 text-center text-gray-400">
            No results found for this query.
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
