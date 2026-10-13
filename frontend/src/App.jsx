import { useState } from 'react'

function App() {
  const [loading, setLoading] = useState(false)
  const [data, setData] = useState(null)
  const [statusMsg, setStatusMsg] = useState("")

  const startAgent = async () => {
    setLoading(true)
    setStatusMsg("Agent is researching and analyzing...")
    try {
      const response = await fetch("http://localhost:8000/start", { method: "POST" })
      const result = await response.json()
      setData(result)
      setStatusMsg("Agent paused. Waiting for human approval.")
    } catch (error) {
      setStatusMsg("Error connecting to Python backend.")
    }
    setLoading(false)
  }

  const handleApproval = async (approved) => {
    setLoading(true)
    setStatusMsg(approved ? "Executing trades..." : "Rejecting trades...")
    try {
      const response = await fetch("http://localhost:8000/approve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ approved })
      })
      const result = await response.json()
      setStatusMsg(result.message)
      setData(null) // Clear dashboard after action
    } catch (error) {
      setStatusMsg("Error communicating with backend.")
    }
    setLoading(false)
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif', maxWidth: '800px', margin: '0 auto' }}>
      <h1>AI Fund Manager Dashboard</h1>
      
      <button 
        onClick={startAgent} 
        disabled={loading}
        style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer', marginBottom: '20px' }}
      >
        {loading ? "Processing..." : "Run Daily Analysis"}
      </button>

      <p style={{ fontWeight: 'bold', color: '#555' }}>{statusMsg}</p>

      {data && (
        <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '8px', marginTop: '20px' }}>
          <h2>📰 Daily News Digest</h2>
          <p style={{ whiteSpace: 'pre-wrap' }}>{data.news_summary}</p>

          <h2>🛡️ Risk Guard Logs</h2>
          <ul style={{ background: '#f5f5f5', padding: '15px', borderRadius: '5px' }}>
            {data.audit_log.map((log, i) => <li key={i}>{log}</li>)}
          </ul>

          <h2>⚖️ Proposed Trades</h2>
          {data.validated_orders.length === 0 ? (
            <p>No valid trades proposed today.</p>
          ) : (
            <ul>
              {data.validated_orders.map((order, i) => (
                <li key={i}>
                  <strong>{order.action}</strong> {order.shares_to_execute} shares of {order.ticker}
                </li>
              ))}
            </ul>
          )}

          {data.validated_orders.length > 0 && (
            <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
              <button 
                onClick={() => handleApproval(true)}
                style={{ background: 'green', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
              >
                Approve & Execute
              </button>
              <button 
                onClick={() => handleApproval(false)}
                style={{ background: 'red', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
              >
                Reject All
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App