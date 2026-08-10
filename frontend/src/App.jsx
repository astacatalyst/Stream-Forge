import { ReactFlow } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const nodes = [
  {
    id: '1',
    position: { x: 100, y: 100 },
    data: { label: 'Worker 1' },
  },
  {
    id: '2',
    position: { x: 300, y: 100 },
    data: { label: 'Worker 2' },
  },
];

const edges = [];

function App() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow nodes={nodes} edges={edges} />
    </div>
  );
}

export default App;