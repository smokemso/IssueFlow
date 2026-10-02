import { useState } from 'react'

function App() {
  const [issues] = useState([
    { id: '1', title: 'App crashes on start', category: 'bug' },
    { id: '2', title: 'Add dark mode', category: 'feature' }
  ]);

  const handleBulkAction = () => {
    console.log("Bulk action triggered for issues:", issues.map(i => i.id));
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>IssueFlow Dashboard</h1>
      <button onClick={handleBulkAction} style={{ marginBottom: '20px', padding: '10px' }}>
        Simulate Bulk Action (Logs to Console)
      </button>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {issues.map(issue => (
          <div key={issue.id} style={{ border: '1px solid #ccc', padding: '10px', borderRadius: '4px' }}>
            <strong>#{issue.id} - {issue.title}</strong> 
            <span style={{ 
              marginLeft: '10px', 
              padding: '2px 8px', 
              background: '#eee', 
              borderRadius: '10px',
              fontSize: '12px'
            }}>
              {issue.category}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
