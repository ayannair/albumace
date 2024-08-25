import React from 'react';

const PercentileCard = ({ percentiles }) => {
  return (
    <div className="percentile-card">
      <h2>Your Percentiles</h2>
      <div className="score-columns">
        <div className="score-col">
          <p>Lyrics Percentile: {percentiles.lyrics_score}%</p>
          <p>Production Percentile: {percentiles.production_score}%</p>
          <p>Vocals Percentile: {percentiles.vocals_score}%</p>
        </div>
        <div className="score-col">
          <p>Concept Percentile: {percentiles.concept_score}%</p>
          <p>Originality Percentile: {percentiles.originality_score}%</p>
          <p>Features Percentile: {percentiles.features_score}%</p>  
        </div>
      </div>
      <div className="score-overall">
        <p>Overall Percentile: {percentiles.overall_score}%</p>
      </div>
    </div>
  );
};

export default PercentileCard;
