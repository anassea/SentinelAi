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
  };

  const thTdStyle = {
    border: '1px solid black',
    padding: '8px',
    textAlign: 'left',
  };

  return (
    <div>
      <h1>Recommendations</h1>
      {recommendations.length > 0 ? (
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={thTdStyle}>Type</th>
              <th style={thTdStyle}>Recommendation</th>
              <th style={thTdStyle}>Time</th>
            </tr>
          </thead>
          <tbody>
            {recommendations.map((rec, index) => (
              <tr key={rec.ID || index}>
                <td style={thTdStyle}>{rec.event_type}</td>
                <td style={thTdStyle}>{rec.recommendation}</td>
                <td style={thTdStyle}>{rec.timestamp}</td>
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
