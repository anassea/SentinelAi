import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Navbar from './components/Navbar';
import Alertes from './components/Lesalertes';
import Incidents from './components/Incidents';
import ReponseIncidents from './components/ReponseIncidents';
import Rapport from './components/Rapport';
import Footer from './components/Footer';
import Dashboard from './components/Dashboard'; // Assuming you have a Dashboard component
import ChatBot from './components/ChatBot';
import './App.css';

const App = () => {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <div className="content">
          <Switch>
            <Route exact path="/" component={Dashboard} />
            <Route path="/Lesalertes" component={Alertes} />
            <Route path="/incidents" component={Incidents} />
            <Route path="/reponse-incidents" component={ReponseIncidents} />
            <Route path="/rapport" component={Rapport} />
            <Route path="/chatbot" component={ChatBot} />
          </Switch>
        </div>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
