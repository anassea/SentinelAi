import React from 'react';

const App = () => {
  return (
    <div className="navbar">
      <h1>SIEM Dashboard</h1>
      <ul>
        <li><a href="/">Accueil</a></li>
        <li><a href="/Lesalertes">Alertes</a></li>
        <li><a href="/incidents">Incidents</a></li>
        <li><a href="/reponse-incidents">Réponse aux incidents</a></li>
        <li><a href="/rapport">Rapport</a></li>
        <li><a href="/chatbot">ChatBot</a></li>
      </ul>
    </div>
  );
};


export default App;
