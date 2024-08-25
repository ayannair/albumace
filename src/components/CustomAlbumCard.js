import React, { useState } from 'react';
import '../styles.css';

const getBarColor = (score) => {
  if (score >= 0 && score <= 39.99) return 'red';
  if (score >= 40 && score <= 69.99) return 'orange';
  if (score >= 70 && score <= 92.99) return 'green';
  if (score >= 93 && score <= 100) return 'purple';
  return 'gray'; // Default color
};

const ScoreSlider = ({ score, label, index, onChange }) => {
  const barColor = getBarColor(score);
  const delay = `${index * 0.5}s`; // Increase delay for each bar

  return (
    <div className="scorebar-container" style={{ '--delay': delay }}>
      <div className="scorebar-label">{label}</div>
      <input
        type="number"
        min="0"
        max="100"
        value={score}
        onChange={(e) => onChange(Number(e.target.value))}
        className="scorebar-input"
      />
      <input
        type="range"
        min="0"
        max="100"
        value={score}
        onChange={(e) => onChange(Number(e.target.value))}
        className="scorebar-slider"
        style={{
          background: `linear-gradient(to right, ${barColor} ${score}%, #e0e0e0 ${score}%)`,
          '--bar-color': barColor // CSS variable for slider thumb color
        }}
      />
      <div className="scorebar-value">{score.toFixed(2)}</div>
    </div>
  );
};

const CustomAlbumCard = ({ initialScores, onSave }) => {
  const [scores, setScores] = useState(initialScores);

  const handleSliderChange = (value, key) => {
    setScores({ ...scores, [key]: value });
  };

  const handleOverallChange = (e) => {
    const value = Math.max(0, Math.min(Number(e.target.value), 100));
    setScores({ ...scores, overall_score: value });
  };

  const handleSave = () => {
    onSave(scores);
  };

  const leftColumn = [
    { score: scores.lyrics_score, label: "Lyrics", key: "lyrics_score" },
    { score: scores.production_score, label: "Production", key: "production_score" },
    { score: scores.vocals_score, label: "Vocals", key: "vocals_score" }
  ];

  const rightColumn = [
    { score: scores.concept_score, label: "Concept", key: "concept_score" },
    { score: scores.originality_score, label: "Originality", key: "originality_score" },
    { score: scores.features_score, label: "Features", key: "features_score" }
  ];

  const overallColor = getBarColor(scores.overall_score);

  return (
    <div className="custom-album-card">
      <div className="scores-section">
        <div className="column">
          {leftColumn.map((scoreLabel, index) => (
            <ScoreSlider
              key={index}
              score={scoreLabel.score}
              label={scoreLabel.label}
              index={index}
              onChange={(value) => handleSliderChange(value, scoreLabel.key)}
            />
          ))}
        </div>
        <div className="overall-score">
          <div className="scorebar-label"></div>
          <input
            type="number"
            min="0"
            max="100"
            value={scores.overall_score}
            onChange={handleOverallChange}
            className="scorebar-input"
          />
          <input
            type="range"
            min="0"
            max="100"
            value={scores.overall_score}
            onChange={handleOverallChange}
            className="scorebar-slider"
            style={{
              background: `linear-gradient(to right, ${overallColor} ${scores.overall_score}%, #e0e0e0 ${scores.overall_score}%)`,
              '--bar-color': overallColor // CSS variable for slider thumb color
            }}
          />
          <div className="scorebar-value">{scores.overall_score.toFixed(2)}</div>
        </div>
        <div className="column">
          {rightColumn.map((scoreLabel, index) => (
            <ScoreSlider
              key={index}
              score={scoreLabel.score}
              label={scoreLabel.label}
              index={index + 3}
              onChange={(value) => handleSliderChange(value, scoreLabel.key)}
            />
          ))}
        </div>
      </div>
      <button onClick={handleSave} className="save-button">Save</button>
    </div>
  );
};

export default CustomAlbumCard;
