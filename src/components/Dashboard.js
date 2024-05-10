import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Chart from 'chart.js/auto';

const Dashboard = () => {
  const [data, setData] = useState({
    aggregatedData: {},
    ipCount: {},
    authenticationMethods: {},
    failedAuthenticationUsers: []
  });

  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const eventsPerHourChartRef = useRef(null);
  const topEventSourcesChartRef = useRef(null);

  useEffect(() => {
    axios.get('http://localhost:5000/get_data')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching report data:', error);
      });
  }, []);

  useEffect(() => {
    const { aggregatedData, ipCount } = data;

    const eventsPerHourData = {
      labels: Object.keys(aggregatedData),
      datasets: [{
        label: 'Événements par heure',
        data: Object.values(aggregatedData),
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    };

    const topEventSourcesData = {
      labels: Object.keys(ipCount),
      datasets: [{
        label: 'Nombre d\'événements',
        data: Object.values(ipCount),
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)'
        ],
        borderWidth: 1
      }]
    };

    if (eventsPerHourChartRef.current) {
      if (eventsPerHourChartRef.current.chart) {
        eventsPerHourChartRef.current.chart.destroy();
      }
      eventsPerHourChartRef.current.chart = new Chart(eventsPerHourChartRef.current, {
        type: 'line',
        data: eventsPerHourData,
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }

    if (topEventSourcesChartRef.current) {
      if (topEventSourcesChartRef.current.chart) {
        topEventSourcesChartRef.current.chart.destroy();
      }
      topEventSourcesChartRef.current.chart = new Chart(topEventSourcesChartRef.current, {
        type: 'bar',
        data: topEventSourcesData,
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }, [data]);

  const handleSearch = () => {
    if (searchQuery.trim() !== '') {
      axios.get(`http://localhost:5000/search_logs?query=${searchQuery}`)
        .then(response => {
          setSearchResults(response.data.results);
        })
        .catch(error => {
          console.error('Error searching logs:', error);
        });
    }
  };

  return (
    <div className="dashboard">
      <h2>Tableau de bord SIEM</h2>

      <div className="summary">
        <div className="summary-card">
          <h3>Total d'événements</h3>
          <p>{data.aggregatedData && data.aggregatedData['success']}</p>
        </div>
        <div className="summary-card">
          <h3>Alertes actives</h3>
          <p>{data.aggregatedData && data.aggregatedData['warning']}</p>
        </div>
        <div className="summary-card">
          <h3>Utilisateurs suspects</h3>
          <p>{data.failedAuthenticationUsers.length}</p>
        </div>
      </div>
      <div className="charts">
        <div className="chart">
          <h3>Événements par heure</h3>
          <canvas ref={eventsPerHourChartRef} width="400" height="200"></canvas>
        </div>
        <div className="chart">
          <h3>Top 10 des sources d'événements</h3>
          <canvas ref={topEventSourcesChartRef} width="400" height="200"></canvas>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
