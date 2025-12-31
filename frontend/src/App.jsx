import React, { useEffect, useState } from 'react';
import { Container, Grid, Paper, Typography, Alert, Chip, Box } from '@mui/material';

function App() {
  const [alerts, setAlerts] = useState([]);
  const [status, setStatus] = useState("Connecting...");

  useEffect(() => {
    // Connect to the Python Backend
    const ws = new WebSocket("ws://localhost:8000/ws/alerts");

    ws.onopen = () => setStatus("🟢 System Live");
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setAlerts((prev) => [data, ...prev].slice(0, 5));
    };

    ws.onclose = () => setStatus("🔴 Disconnected");

    return () => ws.close();
  }, []);

  return (
    <Container maxWidth="xl" sx={{ mt: 4, bgcolor: '#f5f5f5', height: '100vh', pt: 2 }}>
      <Typography variant="h4" fontWeight="bold" gutterBottom color="primary">
        SafetyVision AI Control Center
      </Typography>
      
      <Chip label={status} color={status.includes("🟢") ? "success" : "error"} sx={{ mb: 3 }} />

      <Grid container spacing={3}>
        {/* LEFT: Video Feed */}
        <Grid item xs={12} md={8}>
          <Paper elevation={6} sx={{ p: 1, bgcolor: '#000', border: '4px solid #333' }}>
            <Typography variant="subtitle2" color="white" sx={{ mb: 1 }}>Live Camera Feed - Cam 01</Typography>
            {/* Direct stream from Python */}
            <img 
              src="http://localhost:8000/video_feed" 
              alt="Loading Camera..." 
              style={{ width: '100%', borderRadius: '4px' }} 
            />
          </Paper>
        </Grid>

        {/* RIGHT: Real-Time Alerts */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 2, height: '100%', bgcolor: '#fff' }}>
            <Typography variant="h6" color="error" fontWeight="bold" gutterBottom>
              🚨 Violation Log
            </Typography>
            
            {alerts.length === 0 && (
              <Typography color="text.secondary" sx={{ mt: 2 }}>
                System Secure. No violations detected.
              </Typography>
            )}

            {alerts.map((alert, index) => (
              <Box key={index} mb={1}>
                <Alert severity="error" variant="filled">
                  <strong>{alert.type}</strong>
                  <br />
                  <small>{alert.timestamp} • {alert.zone}</small>
                </Alert>
              </Box>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;