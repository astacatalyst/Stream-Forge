import { useState, useEffect } from 'react';
import { ReactFlow } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

function App() {
  const [backendStatus, setBackendStatus] = useState('checking...');
  const [nodes, setNodes] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/health')
      .then((res) => res.json())
      .then((data) => setBackendStatus(data.status))
      .catch(() => setBackendStatus('unreachable'));
  }, []);

  useEffect(() => {
    fetch('http://localhost:8000/workers')
      .then((res) => res.json())
      .then((workers) => {
        const flowNodes = workers.map((worker, index) => ({
          id: worker.id,
          position: { x: index * 200, y: 100 },
          data: { label: `${worker.label} (${worker.status})` },
          style: {
            background: worker.status === 'healthy' ? '#d1fae5' : '#fee2e2',
            border: worker.status === 'healthy' ? '1px solid #10b981' : '1px solid #ef4444',
          },
        }));
        setNodes(flowNodes);
      })
      .catch(() => setNodes([]));
  }, []);

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <div style={{ padding: '10px', fontFamily: 'sans-serif' }}>
        Backend status: <strong>{backendStatus}</strong>
      </div>
      <div style={{ width: '100%', height: 'calc(100% - 40px)' }}>
        <ReactFlow nodes={nodes} edges={[]} />
      </div>
    </div>
  );
}

export default App;