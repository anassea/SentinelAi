import React from 'react';

const Log = ({ timestamp, message }) => {
  return (
    <div className="log">
      <span className="timestamp">{timestamp}</span>
      <span className="message">{message}</span>
    </div>
  );
};

export default Log;
