import { useState, useEffect } from 'react';
import { ReactFlow } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const nodes = [
  { id: '1', position: { x: 100, y: 100 }, data: { label: 'Worker 1' } },
  { id: '2', position: { x: 300, y: 100 }, data: { label: 'Worker 2' } },
];

const edges = [];

function App() {
  const [backendStatus, setBackendStatus] = useState('checking...');

  useEffect(() => {
    fetch('http://localhost:8000/health')
      .then((res) => res.json())
      .then((data) => setBackendStatus(data.status))
      .catch(() => setBackendStatus('unreachable'));
  }, []);

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <div style={{ padding: '10px', fontFamily: 'sans-serif' }}>
        Backend status: <strong>{backendStatus}</strong>
      </div>
      <div style={{ width: '100%', height: 'calc(100% - 40px)' }}>
        <ReactFlow nodes={nodes} edges={edges} />
      </div>
    </div>
  );
}

export default App;