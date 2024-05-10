import React from 'react';

const Rapport = () => {
  const handleDownload = async () => {
    try {
      const response = await fetch('http://localhost:3000/rapport');
      if (!response.ok) throw new Error('Network response was not ok.');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(new Blob([blob], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'rapport_incident1.pdf');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('Failed to download the file:', error);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '50px', border: '1px solid #ccc', borderRadius: '10px', padding: '20px' }}>
      <h1 style={{ color: '#5844E7', marginBottom: '20px', fontSize: '28px', borderBottom: '2px solid #5844E7', paddingBottom: '10px' }}>Rapport des incidents</h1>
      <button
        onClick={handleDownload}
        style={{
          padding: '12px 24px',
          backgroundColor: '#5844E7',
          color: '#fff',
          border: '1px solid #5844E7',
          borderRadius: '5px',
          cursor: 'pointer',
          fontSize: '18px',
          fontWeight: 'bold',
          boxShadow: '0 2px 5px rgba(0, 0, 0, 0.2)',
          transition: 'background-color 0.3s ease',
        }}
      >
        Télécharger le rapport
      </button>
    </div>
  );
};

export default Rapport;
