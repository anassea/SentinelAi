import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ResponseIncident = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5003/classification-report');
        setData(response.data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!data) {
    return null;
  }

  return (
    <div>
      <h2>Rapport de classification :</h2>
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Précision</th>
            <th>Rappel</th>
            <th>Score F1</th>
            <th>Support</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(data.classification_report).map(([type, metrics]) => (
            <tr key={type}>
              <td>{type}</td>
              <td>{metrics.precision.toFixed(2)}</td>
              <td>{metrics.recall.toFixed(2)}</td>
              <td>{metrics['f1-score'].toFixed(2)}</td>
              <td>{metrics.support}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Recommandations :</h2>
      <table>
        <thead>
          <tr>
            <th>Alerte</th>
            <th>ID</th>
            <th>Type</th>
            <th>Recommandation</th>
          </tr>
        </thead>
        <tbody>
          {data.recommendations.map((recommendation, index) => (
            <tr key={index}>
              <td>{recommendation.Alerte}</td>
              <td>{recommendation.ID}</td>
              <td>{recommendation.Type}</td>
              <td>{recommendation.Recommandation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ResponseIncident;
