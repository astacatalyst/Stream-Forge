import { useState, useEffect, useCallback } from 'react';
import { ReactFlow, Background, Controls } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    fetchTopology();
    const interval = setInterval(fetchTopology, 5000); // refresh every 5s
    return () => clearInterval(interval);
  }, []);

  const fetchTopology = () => {
    fetch('http://localhost:8000/topology')
      .then((res) => res.json())
      .then((data) => buildGraph(data))
      .catch((err) => console.error('Failed to fetch topology', err));
  };

  const buildGraph = (data) => {
    const newNodes = [];
    const newEdges = [];

     // FastAPI source node (top, above Kafka)
    newNodes.push({
      id: data.source.id,
      position: { x: 400, y: -100 },
      data: { label: data.source.label, raw: data.source },
      style: { background: '#f3e8ff', border: '2px solid #9333ea', fontWeight: 'bold' },
    });

    // Dashboard node (off to the side, showing FastAPI feeds the dashboard too)
    newNodes.push({
      id: data.dashboard.id,
      position: { x: 700, y: -100 },
      data: { label: data.dashboard.label },
      style: { background: '#dbeafe', border: '2px solid #2563eb', fontWeight: 'bold' },
    });

    // Edge: source -> dashboard
    newEdges.push({
      id: `e-${data.source.id}-${data.dashboard.id}`,
      source: data.source.id,
      target: data.dashboard.id,
      animated: true,
    });


    // Kafka node (top, center)
    newNodes.push({
      id: data.kafka.id,
      position: { x: 400, y: 0 },
      data: { label: data.kafka.label, raw: data.kafka },
      style: { background: '#fef3c7', border: '2px solid #f59e0b', fontWeight: 'bold' },
    });

    // Edge: source -> kafka
    newEdges.push({
      id: `e-${data.source.id}-${data.kafka.id}`,
      source: data.source.id,
      target: data.kafka.id,
      animated: true,
    });

    
    // Kafka node (top, center)
    newNodes.push({
      id: data.kafka.id,
      position: { x: 400, y: 0 },
      data: { label: data.kafka.label, raw: data.kafka },
      style: { background: '#fef3c7', border: '2px solid #f59e0b', fontWeight: 'bold' },
    });

    // Partition nodes (middle row)
    data.partitions.forEach((p, i) => {
      newNodes.push({
        id: p.id,
        position: { x: i * 250, y: 150 },
        data: { label: `${p.label}\nLag: ${p.lag}`, raw: p },
        style: { background: '#e0e7ff', border: '1px solid #6366f1' },
      });
      newEdges.push({
        id: `e-${data.kafka.id}-${p.id}`,
        source: data.kafka.id,
        target: p.id,
        animated: true,
      });
    });

    // Worker nodes (bottom row)
    data.workers.forEach((w, i) => {
      newNodes.push({
        id: w.id,
        position: { x: i * 250, y: 320 },
        data: { label: `${w.label} (${w.status})\n${w.eventsPerSec} ev/s`, raw: w },
        style: {
          background: w.status === 'healthy' ? '#d1fae5' : '#fee2e2',
          border: w.status === 'healthy' ? '1px solid #10b981' : '1px solid #ef4444',
        },
      });
      newEdges.push({
        id: `e-${w.partition}-${w.id}`,
        source: w.partition,
        target: w.id,
        animated: w.status === 'healthy',
      });
    });

    setNodes(newNodes);
    setEdges(newEdges);
  };

  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node.data.raw);
  }, []);
  const [activeTab, setActiveTab] = useState('nodes'); 

  const [tempData, setTempData] = useState([]);

  useEffect(() => {
    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchTelemetry = () => {
    fetch('http://localhost:8000/telemetry')
      .then((res) => res.json())
      .then((trucks) => {
        // Reshape data: one row per timestamp, one column per truck
        const merged = trucks[0].readings.map((_, i) => {
          const point = { time: new Date(trucks[0].readings[i].time * 1000).toLocaleTimeString() };
          trucks.forEach((truck) => {
            point[truck.truck_id] = truck.readings[i].temp;
          });
          return point;
        });
        setTempData(merged);
      })
      .catch((err) => console.error('Failed to fetch telemetry', err));
  };

  const [nodesAnalysis, setNodesAnalysis] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/nodes-analysis')
      .then((res) => res.json())
      .then(setNodesAnalysis)
      .catch((err) => console.error('Failed to fetch nodes analysis', err));
  }, []);

  const [locations, setLocations] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/locations')
      .then((res) => res.json())
      .then(setLocations)
      .catch((err) => console.error('Failed to fetch locations', err));
  }, []);


  return (
    <div style={{ width: '100vw', height: '100vh', fontFamily: 'sans-serif', display: 'flex', flexDirection: 'column' }}>
      <div style={{ padding: '12px 16px', borderBottom: '1px solid #ddd' }}>
        <h2 style={{ margin: '0 0 10px' }}>StreamForge Dashboard</h2>
        <div style={{ display: 'flex', gap: '8px' }}>
          {['nodes', 'location', 'temperature', 'dag'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                padding: '8px 16px',
                border: '1px solid #ccc',
                borderRadius: '6px',
                background: activeTab === tab ? '#2563eb' : '#f3f4f6',
                color: activeTab === tab ? 'white' : '#111',
                cursor: 'pointer',
                textTransform: 'capitalize',
              }}
            >
              {tab === 'nodes' ? 'Working Nodes' : tab}
            </button>
          ))}
        </div>
      </div>

      <div style={{ flex: 1, overflow: 'auto' }}>
        {activeTab === 'nodes' && nodesAnalysis && (
  <div style={{ padding: '16px' }}>
    <div style={{ display: 'flex', gap: '16px', marginBottom: '20px' }}>
      <div style={{ padding: '16px 24px', background: '#f3f4f6', borderRadius: '8px' }}>
        <div style={{ fontSize: '28px', fontWeight: 'bold' }}>{nodesAnalysis.total}</div>
        <div style={{ color: '#666' }}>Total workers</div>
      </div>
      <div style={{ padding: '16px 24px', background: '#d1fae5', borderRadius: '8px' }}>
        <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#059669' }}>{nodesAnalysis.healthy}</div>
        <div style={{ color: '#666' }}>Healthy</div>
      </div>
      <div style={{ padding: '16px 24px', background: '#fee2e2', borderRadius: '8px' }}>
        <div style={{ fontSize: '28px', fontWeight: 'bold', color: '#dc2626' }}>{nodesAnalysis.down}</div>
        <div style={{ color: '#666' }}>Down</div>
      </div>
    </div>

    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ textAlign: 'left', borderBottom: '2px solid #ddd' }}>
          <th style={{ padding: '8px' }}>Worker</th>
          <th style={{ padding: '8px' }}>Status</th>
          <th style={{ padding: '8px' }}>Events/sec</th>
          <th style={{ padding: '8px' }}>Uptime</th>
        </tr>
      </thead>
      <tbody>
        {nodesAnalysis.workers.map((w) => (
          <tr key={w.id} style={{ borderBottom: '1px solid #eee' }}>
            <td style={{ padding: '8px' }}>{w.label}</td>
            <td style={{ padding: '8px', color: w.status === 'healthy' ? '#059669' : '#dc2626' }}>
              {w.status}
            </td>
            <td style={{ padding: '8px' }}>{w.eventsPerSec}</td>
            <td style={{ padding: '8px' }}>{w.uptime}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)}
        {activeTab === 'location' && (
  <div style={{ padding: '16px' }}>
    <h3 style={{ margin: '0 0 16px' }}>Truck locations (live)</h3>
    <div style={{
      position: 'relative',
      width: '100%',
      height: '400px',
      background: '#f0fdf4',
      border: '1px solid #ccc',
      borderRadius: '8px',
      overflow: 'hidden',
    }}>
      {locations.map((truck) => {
        // Normalize lat/lng into a 0-100% position within the box
        const left = ((truck.lng - 78.35) / (78.55 - 78.35)) * 100;
        const top = 100 - ((truck.lat - 17.30) / (17.45 - 17.30)) * 100;
        return (
          <div
            key={truck.truck_id}
            title={`${truck.truck_id} — ${truck.speed} km/h`}
            style={{
              position: 'absolute',
              left: `${left}%`,
              top: `${top}%`,
              transform: 'translate(-50%, -50%)',
              width: '14px',
              height: '14px',
              borderRadius: '50%',
              background: truck.status === 'moving' ? '#10b981' : '#f59e0b',
              border: '2px solid white',
              boxShadow: '0 0 4px rgba(0,0,0,0.3)',
              cursor: 'pointer',
            }}
          />
        );
      })}
    </div>
    <div style={{ marginTop: '12px', display: 'flex', gap: '16px', fontSize: '14px' }}>
      <span><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', background: '#10b981', marginRight: '6px' }}></span>Moving</span>
      <span><span style={{ display: 'inline-block', width: '10px', height: '10px', borderRadius: '50%', background: '#f59e0b', marginRight: '6px' }}></span>Idle</span>
    </div>
  </div>
)}
        {activeTab === 'temperature' && (
  <div style={{ width: '100%', height: '100%', padding: '16px', boxSizing: 'border-box' }}>
    <h3 style={{ margin: '0 0 8px' }}>Live truck temperatures</h3>
    <ResponsiveContainer width="100%" height="90%">
      <LineChart data={tempData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="truck-1" stroke="#ef4444" />
        <Line type="monotone" dataKey="truck-2" stroke="#3b82f6" />
        <Line type="monotone" dataKey="truck-3" stroke="#10b981" />
      </LineChart>
    </ResponsiveContainer>
  </div>
)}
        {activeTab === 'dag' && (
  <div style={{ width: '100%', height: '100%', display: 'flex' }}>
    <div style={{ flex: 1 }}>
      <ReactFlow nodes={nodes} edges={edges} onNodeClick={onNodeClick} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
    {selectedNode && (
      <div style={{ width: '280px', padding: '16px', borderLeft: '1px solid #ddd' }}>
        <h3>Details</h3>
        <pre style={{ whiteSpace: 'pre-wrap', fontSize: '13px' }}>
          {JSON.stringify(selectedNode, null, 2)}
        </pre>
        <button onClick={() => setSelectedNode(null)}>Close</button>
      </div>
    )}
  </div>
)}
      </div>
    </div>
  );
}

export default App;