import { useState } from 'react'; // sandamis comment
import axios from 'axios';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null); 
  const [loading, setLoading] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState(false);

  // Logic to handle text changes - auto-reset if text is cleared
  const handleInputChange = (e) => {
    const newValue = e.target.value;
    setInput(newValue);

    if (newValue.trim() === '') {
      setResult(null);
      setFeedbackGiven(false);
    }
  };

  // Logic for the "Clear" button
  const handleClear = () => {
    setInput('');
    setResult(null);
    setFeedbackGiven(false);
  };

  const handleAnalyze = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setResult(null);
    setFeedbackGiven(false);

    try {
      const response = await axios.post(`${API_URL}/api/resolve/analyze`, {
        problemText: input
      });
      setResult(response.data);
    } catch (err) {
      alert("Could not connect to the backend. Is it running?");
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (isHelpful) => {
    try {
      await axios.post(`${API_URL}/api/resolve/feedback`, {
        logId: result.logId,
        wasHelpful: isHelpful
      });
      setFeedbackGiven(true);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <div className="logo-container">
          <img src="/logo.png" alt="SilverMoonAI Logo" className="logo" />
        </div>
        <h1>SilverMoon </h1>
        <p>Your smart relationship assistant</p>
      </header>

      <div className="card">
        <textarea
          placeholder="Tell me what's wrong... (e.g., 'He never listens to me')"
          value={input}
          onChange={handleInputChange} 
          rows="4"
        />

        <div className="button-group">
          <button 
            className="btn-primary" 
            onClick={handleAnalyze} 
            disabled={loading || !input}
          >
            {loading ? 'Thinking...' : (
              <>
                🔍 Solution
              </>
              // sandami
            )}
          </button>
          <button 
            className="btn-clear" 
            onClick={handleClear}
            disabled={!input}
          >
            🗑️ Clear
          </button>
        </div>
      </div>

      {result && (
        <div className="result-card fade-in">
          <div className="category-badge">{result.category}</div>
          <h3>Suggested Solutions:</h3>
          <ul>
            {result.suggestions.map((sol, index) => (
              <li key={index}>{sol}</li>
            ))}
          </ul>

          <div className="feedback-section">
            {!feedbackGiven ? (
              <>
                <p className="feedback-text">Was this helpful?</p>
                <div className="feedback-buttons">
                  <button className="btn-thumb" onClick={() => handleFeedback(true)}>👍 Yes</button>
                  <button className="btn-thumb" onClick={() => handleFeedback(false)}>👎 No</button>
                </div>
              </>
            ) : (
              <p className="thanks-msg">✅ Thanks for your feedback!</p>
            )}
          </div>
        </div>
      )}

      <footer className="footer">
        <p className="footer-text">Upeksha & Praveen | Proj - CoupleCore - Data Collecting Phase | December 2025</p>
      </footer>
    </div>
  );
}

export default App;
