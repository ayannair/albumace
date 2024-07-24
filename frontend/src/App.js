import React, { useState } from 'react';
import './styles.css';
import axios from 'axios';

const App = () => {
  const [query, setQuery] = useState('');
  const [scores, setScores] = useState(null); // Store all scores
  const [youtubeLink, setYoutubeLink] = useState(''); // Store YouTube link
  const [loading, setLoading] = useState(false); // Store loading state

  const handleSearch = async () => {
    setScores(null); // Clear previous results
    setYoutubeLink(''); // Clear previous video
    setLoading(true); // Set loading indicator to true

    try {
      const response = await axios.get(`http://127.0.0.1:5000/search?query=${query}`);
      console.log(response.data);
      const { concept_score, features_score, lyrics_score, overall_score, production_score, vocals_score } = response.data['score']; // Deconstruct the response data
      const ytlink = response.data['link'];
      setScores({ concept_score, features_score, lyrics_score, overall_score, production_score, vocals_score }); // Update scores with the scores from response
      setYoutubeLink(ytlink); // Set the YouTube link
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false); // Set loading indicator to false
    }
  };

  const getBarColor = (score) => {
    if (score >= 0 && score <= 39.99) return 'red';
    if (score >= 40 && score <= 69.99) return 'orange';
    if (score >= 70 && score <= 92.99) return 'green';
    if (score >= 93 && score <= 100) return 'purple';
    return 'gray'; // Default color
  };

  const ScoreBar = ({ score, label }) => {
    const validScore = Math.max(0, Math.min(score, 100));
    const barWidth = `${validScore}%`;
    const barColor = getBarColor(validScore);

    return (
      <div className="scorebar-container">
        <div className="scorebar-label">{label}</div>
        <div className="scorebar-bar">
          <div className="scorebar-fill" style={{ width: barWidth, backgroundColor: barColor }}>
            <span className="scorebar-text">{validScore.toFixed(2)}</span>
          </div>
        </div>
      </div>
    );
  };

  const embedYTLink = (regularLink) => {
    const videoId = regularLink.split('v=')[1];
    return `https://www.youtube.com/embed/${videoId}`;
  };

  return (
    <div className="container">
      <h1>Fantanosize</h1>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search an Album..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      {loading && <div className="loading">Loading...</div>} {/* Show loading indicator */}
      {!loading && scores && (
        <div className="scores-container">
          <ScoreBar score={scores.lyrics_score} label="Lyrics" />
          <ScoreBar score={scores.production_score} label="Production" />
          <ScoreBar score={scores.features_score} label="Features" />
          <ScoreBar score={scores.vocals_score} label="Vocals" />
          <ScoreBar score={scores.concept_score} label="Concept" />
          <ScoreBar score={scores.overall_score} label="Overall" />
        </div>
      )}
      {!loading && youtubeLink && (
        <div className="video-player">
          <h2>Watch the Review Yourself</h2>
          <iframe
            width="560"
            height="315"
            src={embedYTLink(youtubeLink)}
            title="YouTube video player"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
      )}
    </div>
  );
};

export default App;
