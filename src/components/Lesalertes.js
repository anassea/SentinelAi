import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Lesalertes = () => {
  const [logData, setLogData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    axios.get('/log.json')
      .then(response => {
        if (!response.data || response.data.length === 0) {
          console.error("No data in log.json or data is empty");
          return;
        }
        const normalizedLogs = normalizeData(response.data);
        const aggregatedLogs = aggregateData(normalizedLogs);
        setLogData(Object.values(aggregatedLogs));
        setFilteredData(Object.values(aggregatedLogs));
      })
      .catch(error => {
        console.error('Failed to load log data:', error);
      });
  }, []);

  const normalizeData = (logs) => logs.map(log => ({
    ...log,
    resource_usage: {
      cpu: parseInt(log.resource_usage.cpu.replace('%', '')),
      ram: parseInt(log.resource_usage.ram.replace('%', '')),
      storage: parseInt(log.resource_usage.storage.replace('%', ''))
    }
  }));

  const aggregateData = (normalizedLogs) => {
    return normalizedLogs.reduce((acc, log) => {
      const key = `${log.event_type}-${log.user_id}`;
      if (!acc[key]) {
        acc[key] = { ...log, count: 1, ips: new Set([log.ip_address]) };
      } else {
        acc[key].count++;
        acc[key].ips.add(log.ip_address);
        acc[key].resource_usage.cpu += log.resource_usage.cpu;
        acc[key].resource_usage.ram += log.resource_usage.ram;
        acc[key].resource_usage.storage += log.resource_usage.storage;
      }
      return acc;
    }, {});
  };

  const handleSearch = (event) => {
    const value = event.target.value.toLowerCase();
    setSearchTerm(value);
    const filtered = logData.filter(log =>
      (log.event_type && log.event_type.toLowerCase().includes(value)) ||
      (log.user_id && log.user_id.toLowerCase().includes(value)) ||
      (log.ips && Array.from(log.ips).some(ip => ip && ip.includes(value)))
    );
    setFilteredData(filtered);
  };

  return (
    <div style={{ margin: '20px', padding: '20px', border: '1px solid #ccc', borderRadius: '10px', boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)' }}>
      <h1 style={{ fontSize: '32px', marginBottom: '20px', textAlign: 'center', color: '#5844E7' }}>SIEM Dashboard - Event Log Details</h1>
      <input
        type="text"
        placeholder="Search logs..."
        value={searchTerm}
        onChange={handleSearch}
        style={{ marginBottom: '20px', padding: '12px', width: '100%', boxSizing: 'border-box', borderRadius: '5px', border: '2px solid #5844E7', fontSize: '16px' }}
      />
      {filteredData.length > 0 ? (
        <table style={{ width: '100%', borderCollapse: 'collapse', boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)', borderRadius: '10px' }}>
          <thead>
            <tr style={{ backgroundColor: '#5844E7', color: '#fff' }}>
              <th style={{ padding: '15px', textAlign: 'left', borderBottom: '2px solid #fff' }}>Event Type</th>
              <th style={{ padding: '15px', textAlign: 'left', borderBottom: '2px solid #fff' }}>User ID</th>
              <th style={{ padding: '15px', textAlign: 'left', borderBottom: '2px solid #fff' }}>Occurrences</th>
              <th style={{ padding: '15px', textAlign: 'left', borderBottom: '2px solid #fff' }}>CPU Avg (%)</th>
              <th style={{ padding: '15px', textAlign: 'left', borderBottom: '2px solid #fff' }}>RAM Avg (%)</th>
              <th style={{ padding: '15px', textAlign: 'left', borderBottom: '2px solid #fff' }}>Storage Avg (%)</th>
              <th style={{ padding: '15px', textAlign: 'left', borderBottom: '2px solid #fff' }}>IP Addresses</th>
            </tr>
          </thead>
          <tbody>
            {filteredData.map((log, index) => (
              <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#ffd8b1' : '#fff' }}>
                <td style={{ padding: '15px' }}>{log.event_type}</td>
                <td style={{ padding: '15px' }}>{log.user_id}</td>
                <td style={{ padding: '15px' }}>{log.count}</td>
                <td style={{ padding: '15px' }}>{Math.round(log.resource_usage.cpu / log.count)}</td>
                <td style={{ padding: '15px' }}>{Math.round(log.resource_usage.ram / log.count)}</td>
                <td style={{ padding: '15px' }}>{Math.round(log.resource_usage.storage / log.count)}</td>
                <td style={{ padding: '15px' }}>{log.ips ? Array.from(log.ips).join(', ') : 'No IPs recorded'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p style={{ fontStyle: 'italic', color: '#999', textAlign: 'center', fontSize: '18px', marginTop: '30px' }}>No results found.</p>
      )}
    </div>
  );
};

export default Lesalertes;
