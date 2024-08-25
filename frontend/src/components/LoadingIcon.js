import React, { useState, useEffect } from 'react';
import { PulseLoader } from 'react-spinners';
import '../styles.css';

const LoadingIcon = ({ loading }) => {
  const [textIndex, setTextIndex] = useState(0);
  const loadingTexts = [
    "Fetching album data...",
    "Scoring album...",
    "Displaying songs..."
  ];

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setTextIndex(prevIndex => (prevIndex + 1) % loadingTexts.length);
      }, 1500); // Change text every 1.5 seconds

      return () => clearInterval(interval); // Clean up interval on component unmount
    }
  }, [loading, loadingTexts.length]);

  return (
    <div className="loading-icon">
      <PulseLoader color="#36D7B7" loading={loading} />
      {loading && (
        <div className="loading-text">
          {loadingTexts[textIndex]}
        </div>
      )}
    </div>
  );
};

export default LoadingIcon;
