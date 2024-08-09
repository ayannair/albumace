import React, { useState } from 'react';
import './styles.css';
import axios from 'axios';
import LoadingIcon from './components/LoadingIcon';
import AlbumCard from './components/AlbumCard';
import CustomAlbumCard from './components/CustomAlbumCard';

const App = () => {
  const [query, setQuery] = useState('');
  const [scores, setScores] = useState(null);
  const [customScores, setCustomScores] = useState(null);
  const [lyrics, setLyrics] = useState(null);
  const [selectedSong, setSelectedSong] = useState(null);
  const [topics, setTopics] = useState({});
  const [loading, setLoading] = useState(false);
  const [showTopics, setShowTopics] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [editingScores, setEditingScores] = useState(false);

  const handleInputChange = async (e) => {
    const value = e.target.value;
    setQuery(value);

    if (value.length > 1) {
      try {
        const response = await axios.get('http://127.0.0.1:5000/autocomplete', {
          params: { query: value }
        });
        setSuggestions(response.data);
      } catch (error) {
        console.error('Error fetching suggestions:', error);
      }
    } else {
      setSuggestions([]);
    }
  };

  const handleSearch = async () => {
    setScores(null);
    setLyrics(null);
    setSelectedSong(null);
    setTopics({});
    setLoading(true);
    setCustomScores(null);

    try {
      const response = await axios.get(`http://127.0.0.1:5000/search?query=${query}`);
      console.log(response.data);

      const { concept_score, features_score, lyrics_score, originality_score, overall_score, production_score, vocals_score } = response.data['score'];
      const lyricsData = response.data['lyrics'];

      setScores({ concept_score, features_score, lyrics_score, originality_score, overall_score, production_score, vocals_score });
      setLyrics(lyricsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSongClick = async (songTitle) => {
    setShowTopics(false);

    try {
      const response = await axios.get('http://127.0.0.1:5000/get_topic', {
        params: { song_title: songTitle },
      });
      setTopics(prevTopics => ({ ...prevTopics, [songTitle]: response.data.topic }));
      setSelectedSong(songTitle);
    } catch (error) {
      console.error('Error fetching topic:', error);
    } finally {
      setLoading(false);
      setTimeout(() => setShowTopics(true), 500);
    }
  };

  const sortedLyrics = lyrics ? Object.entries(lyrics).sort(([aIndex], [bIndex]) => aIndex - bIndex) : [];

  const handleSaveScores = async (newScores) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/save_scores', {
        title: query,
        scores: newScores,
      });

      console.log(response.data);
      if(response.data['updated_scores']){
        const { concept_score, features_score, lyrics_score, originality_score, overall_score, production_score, vocals_score } = response.data['updated_scores'];
        setScores({ concept_score, features_score, lyrics_score, originality_score, overall_score, production_score, vocals_score });
      }
    } catch (error) {
      console.error('Error saving scores:', error);
    }

    setCustomScores(newScores);
    setEditingScores(false);
  };



  return (
    <div className="container">
      <div className="header">
        <h1>Fantanosize</h1>
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search an Album..."
            value={query}
            onChange={handleInputChange}
          />
          <button onClick={handleSearch}>Search</button>
          {suggestions.length > 0 && (
            <ul className="autocomplete-suggestions">
              {suggestions.map((suggestion, index) => (
                <li
                  key={index}
                  onClick={() => {
                    setQuery(suggestion);
                    setSuggestions([]);
                  }}
                >
                  {suggestion}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      {loading && <LoadingIcon loading={loading} />}
      <div className="bento-box">
        <div className="left-section">
          {lyrics && (
            <div className="lyrics-table">
              <h2>Songs</h2>
              <table>
                <tbody>
                  {sortedLyrics.map(([index, { title }]) => (
                    <tr key={index}>
                      <td>{title}</td>
                      <td>
                        <button
                          className="get-topics-button"
                          onClick={() => handleSongClick(title)}
                        >
                          {topics[title] ? 'View Topics' : 'Get Topics'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
        <div className="right-section">
          {scores && <AlbumCard scores={scores} />}
          {selectedSong && topics[selectedSong] && (
            <div className={`topics-section ${showTopics ? 'fade-in' : 'fade-out'}`}>
              <h2>{selectedSong} is about...</h2>
              <ul>
                {topics[selectedSong].split('\n').map((topic, index) => (
                  <li key={index}>{topic}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
      <div className="custom-album-card-container">
        {scores && !loading && (
            <button onClick={() => setEditingScores(!editingScores)} className="edit-scores-button">
              {editingScores ? 'View Scores' : 'Edit Scores'}
            </button>
          )}
        {!loading && (
          editingScores ? (
            <CustomAlbumCard initialScores={customScores || scores} onSave={handleSaveScores} />
          ) : (
            <AlbumCard scores={customScores || scores} />
          )
        )}
      </div>
    </div>
  );  
};

export default App;
