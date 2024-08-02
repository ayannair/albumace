import React, { useState, useEffect } from 'react';
import '../styles.css';

const LoadingIcon = ({ loading }) => {
  const [textIndex, setTextIndex] = useState(0);
  const loadingTexts = [
    "Will he love it?",
    "Will he hate it?",
    "What will he rate it?"
  ];

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setTextIndex(prevIndex => (prevIndex + 1) % 3);
      }, 4500); // Change text every 1.5 seconds

      return () => clearInterval(interval); // Clean up interval on component unmount
    }
  }, [loading]); // Removed loadingTexts.length from dependency array

  return (
    <div className="loading-icon">
      <img src={`${process.env.PUBLIC_URL}/fantano.jpeg`} alt="Loading..." className="rotating-image" />
      {loading && (
        <div className="loading-text">
          {loadingTexts[textIndex]}
        </div>
      )}
    </div>
  );
};

export default LoadingIcon;
