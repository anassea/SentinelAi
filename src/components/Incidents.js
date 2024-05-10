import React from 'react';

function Incidents() {
  const tableStyle = {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '20px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    borderRadius: '5px',
  };

  const thStyle = {
    backgroundColor: '#5844E7',
    color: '#fff',
    padding: '10px',
    textAlign: 'left',
    borderBottom: '2px solid #fff',
  };

  const tdStyle = {
    padding: '10px',
    textAlign: 'left',
    borderBottom: '1px solid #ccc',
  };

  const normalStyle = {
    backgroundColor: '#fff',
    color: '#333',
  };

  const mediumStyle = {
    backgroundColor: '#ffd8b1',
    color: '#333',
  };

  return (
    <div>
      <h2 style={{ color: '#5844E7' }}>Liste des incidents</h2>
      <table style={tableStyle}>
        <thead>
          <tr>
            <th style={thStyle}>Timestamp</th>
            <th style={thStyle}>Message</th>
            <th style={thStyle}>Anomaly Score</th>
            <th style={thStyle}>Criticality</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style={{ ...tdStyle, ...normalStyle }}>2024-04-30 08:12:05</td>
            <td style={{ ...tdStyle, ...normalStyle }}>Connexion utilisateur réussie</td>
            <td style={{ ...tdStyle, ...normalStyle }}>0.1260433416661756</td>
            <td style={{ ...tdStyle, ...normalStyle }}>normal</td>
          </tr>
          <tr>
            <td style={{ ...tdStyle, ...normalStyle }}>2024-04-30 08:18:45</td>
            <td style={{ ...tdStyle, ...normalStyle }}>Taux d'utilisation du CPU élevé</td>
            <td style={{ ...tdStyle, ...normalStyle }}>0.09735059447519256</td>
            <td style={{ ...tdStyle, ...normalStyle }}>normal</td>
          </tr>
          <tr>
            <td style={{ ...tdStyle, ...normalStyle }}>2024-04-30 08:20:10</td>
            <td style={{ ...tdStyle, ...normalStyle }}>Tentative de connexion infructueuse</td>
            <td style={{ ...tdStyle, ...normalStyle }}>0.07756886986156564</td>
            <td style={{ ...tdStyle, ...normalStyle }}>normal</td>
          </tr>
          <tr>
            <td style={{ ...tdStyle, ...mediumStyle }}>2024-04-30 08:22:55</td>
            <td style={{ ...tdStyle, ...mediumStyle }}>Erreur lors de l'accès à la base de données</td>
            <td style={{ ...tdStyle, ...mediumStyle }}>-0.007671646469825211</td>
            <td style={{ ...tdStyle, ...mediumStyle }}>medium</td>
          </tr>
          <tr>
            <td style={{ ...tdStyle, ...normalStyle }}>2024-04-30 08:12:05</td>
            <td style={{ ...tdStyle, ...normalStyle }}>Connexion utilisateur réussie</td>
            <td style={{ ...tdStyle, ...normalStyle }}>0.1260433416661756</td>
            <td style={{ ...tdStyle, ...normalStyle }}>normal</td>
          </tr>
          <tr>
            <td style={{ ...tdStyle, ...normalStyle }}>2024-04-30 08:18:45</td>
            <td style={{ ...tdStyle, ...normalStyle }}>Sauvegarde automatique des données effectuée avec succès</td>
            <td style={{ ...tdStyle, ...normalStyle }}>0.1554969420056741</td>
            <td style={{ ...tdStyle, ...normalStyle }}>normal</td>
          </tr>
          <tr>
            <td style={{ ...tdStyle, ...normalStyle }}>2024-04-30 08:20:10</td>
            <td style={{ ...tdStyle, ...normalStyle }}>Mise à jour du logiciel effectuée</td>
            <td style={{ ...tdStyle, ...normalStyle }}>0.1551685216736859</td>
            <td style={{ ...tdStyle, ...normalStyle }}>normal</td>
          </tr>
          <tr>
            <td style={{ ...tdStyle, ...normalStyle }}>2024-04-30 08:22:55</td>
            <td style={{ ...tdStyle, ...normalStyle }}>Requête de recherche traitée</td>
            <td style={{ ...tdStyle, ...normalStyle }}>0.13096668377120047</td>
            <td style={{ ...tdStyle, ...normalStyle }}>normal</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Incidents;
