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

const AlbumCard = ({ scores }) => {
  if (!scores) return <div></div>;

  const leftColumn = [
    { score: scores.lyrics_score || 0, label: "Lyrics" },
    { score: scores.production_score || 0, label: "Production" },
    { score: scores.vocals_score || 0, label: "Vocals" }
  ];

  const rightColumn = [
    { score: scores.concept_score || 0, label: "Concept" },
    { score: scores.originality_score || 0, label: "Originality" },
    { score: scores.features_score || 0, label: "Features" }
  ];

  const overallColor = getBarColor(scores.overall_score || 0);

  return (
    <div className="album-card">
      <div className="scores-section">
        <div className="column">
          {leftColumn.map((scoreLabel, index) => (
            <ScoreBar key={index} score={scoreLabel.score} label={scoreLabel.label} index={index} />
          ))}
        </div>
        <div className="overall-score" style={{ color: overallColor }}>
          {scores.overall_score ? scores.overall_score.toFixed(2) : 'N/A'}
        </div>
        <div className="column">
          {rightColumn.map((scoreLabel, index) => (
            <ScoreBar key={index} score={scoreLabel.score} label={scoreLabel.label} index={index + 3} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default AlbumCard;
