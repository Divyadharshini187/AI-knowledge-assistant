// ai-partn.js
const { useState } = React;

function App() {
  const [note, setNote] = useState('');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const saveNote = async () => {
    if (!note.trim()) return;
    await axios.post('http://localhost:5000/api/save_note', { note });
    setNote('');
  };

  const askQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);
    const res = await axios.post('http://localhost:5000/api/query', { query });
    setResponse(res.data.answer);
    setLoading(false);
  };

  // Return some JSX UI
  return (
    <div className="card">
      <h1>Personal Knowledge Assistant</h1>
      <textarea
        placeholder="Write a note..."
        value={note}
        onChange={e => setNote(e.target.value)}
      />
      <button className="save" onClick={saveNote}>Save Note</button>
      <input
        type="text"
        placeholder="Ask a question..."
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <button className="ask" onClick={askQuery} disabled={loading}>
        {loading ? 'Thinking...' : 'Ask'}
      </button>
      {response && <div className="response">{response}</div>}
    </div>
  );
}

// Render the App component to the DOM
const root = document.getElementById('root');
ReactDOM.createRoot(root).render(<App />);
