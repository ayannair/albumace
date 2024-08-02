import React from 'react';
import '../styles.css';

const getBarColor = (score) => {
  if (score >= 0 && score <= 39.99) return 'red';
  if (score >= 40 && score <= 69.99) return 'orange';
  if (score >= 70 && score <= 92.99) return 'green';
  if (score >= 93 && score <= 100) return 'purple';
  return 'gray'; // Default color
};

const ScoreBar = ({ score, label, index }) => {
  const validScore = Math.max(0, Math.min(score, 100));
  const barWidth = `${validScore}%`;
  const barColor = getBarColor(validScore);
  const delay = `${index * 0.5}s`; // Increase delay for each bar

  return (
    <div className="scorebar-container" style={{ '--delay': delay }}>
      <div className="scorebar-label">{label}</div>
      <div className="scorebar-bar">
        <div className="scorebar-fill" style={{ width: barWidth, backgroundColor: barColor }}>
          <span className="scorebar-text">{validScore.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
};

const ScoreBars = ({ scores }) => {
  const leftColumn = [
    { score: scores.lyrics_score, label: "Lyrics" },
    { score: scores.production_score, label: "Production" },
    { score: scores.vocals_score, label: "Vocals" }
  ];

  const rightColumn = [
    { score: scores.concept_score, label: "Concept" },
    { score: scores.originality_score, label: "Originality" },
    { score: scores.features_score, label: "Features" }
  ];

  const overallColor = getBarColor(scores.overall_score);

  return (
    <div className="album-card">
      <div className="scores-section">
        <div className="column">
          {leftColumn.map((scoreLabel, index) => (
            <ScoreBar key={index} score={scoreLabel.score} label={scoreLabel.label} index={index} />
          ))}
        </div>
        <div className="overall-score" style={{ color: overallColor }}>
          {scores.overall_score.toFixed(2)}
        </div>
        <div className="column">
          {rightColumn.map((scoreLabel, index) => (
            <ScoreBar key={index} score={scoreLabel.score} label={scoreLabel.label} index={index} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ScoreBars;
