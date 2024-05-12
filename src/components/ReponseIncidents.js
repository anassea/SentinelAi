import React, { useEffect, useState } from 'react';

function ReponseIncidents() {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5003/classification-report')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch: ' + response.status);
        }
        return response.json();
      })
      .then(data => {
        if (data.length === 0) {
          console.log('No recommendations found.');
        }
        setRecommendations(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const tableStyle = {
    width: '100%',
    borderCollapse: 'collapse',
    backgroundColor: '#ffffff', // Arrière-plan blanc
  };

  const thTdStyle = {
    borderLeft: '1px solid black', // Bordure à gauche
    borderRight: '1px solid black', // Bordure à droite
    borderBottom: '1px solid black', // Bordure en bas
    padding: '8px',
    textAlign: 'left',
  };

  const headerRowStyle = {
    backgroundColor: '#5844E7',
    color: 'white',
    border: '1px solid black', // Bordure sur tous les côtés pour la ligne d'en-tête
  };

  return (
    <div>
      <h1>Recommendations</h1>
      {recommendations.length > 0 ? (
        <table style={tableStyle}>
          <thead>
            <tr style={headerRowStyle}>
              <th style={thTdStyle}>Time</th>
              <th style={thTdStyle}>Type</th>
              <th style={thTdStyle}>Message</th>
              <th style={thTdStyle}>User ID</th>
              <th style={thTdStyle}>IP Address</th>
              <th style={thTdStyle}>Recommendation</th>
            </tr>
          </thead>
          <tbody>
            {recommendations.map((rec, index) => (
              <tr key={rec.ID || index} style={thTdStyle}>
                <td>{rec.timestamp}</td>
                <td>{rec.event_type}</td>
                <td>{rec.message}</td>
                <td>{rec.user_id}</td>
                <td>{rec.ip_address}</td>
                <td>{rec.recommendation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No recommendations available.</p>
      )}
    </div>
  );
}

export default ReponseIncidents;
