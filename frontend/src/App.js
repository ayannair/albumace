import React, { useState, useEffect } from 'react';
import './styles.css';
import axios from 'axios';
import LoadingIcon from './components/LoadingIcon';
import ScoreBars from './components/ScoreBars';

const App = () => {
  const [query, setQuery] = useState('');
  const [scores, setScores] = useState(null);
  const [lyrics, setLyrics] = useState(null);
  const [selectedSong, setSelectedSong] = useState(null);
  const [topics, setTopics] = useState({});
  const [coverArtUrl, setCoverArtUrl] = useState(null);
  const [coverArt, setCoverArt] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setScores(null);
    setLyrics(null);
    setSelectedSong(null);
    setTopics({});
    setCoverArtUrl(null);
    setCoverArt(null);
    setLoading(true);

    try {
      const response = await axios.get(`http://127.0.0.1:5000/search?query=${query}`);
      console.log(response.data);

      const { concept_score, features_score, lyrics_score, originality_score, overall_score, production_score, vocals_score } = response.data['score'][2];
      const lyricsData = response.data['lyrics'];
      const coverArtPath = response.data['cover_art_url'];

      setScores({ concept_score, features_score, lyrics_score, originality_score, overall_score, production_score, vocals_score });
      setLyrics(lyricsData);
      setCoverArtUrl(coverArtPath);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (coverArtUrl) {
      downloadImage(coverArtUrl).then(imageBlob => {
        setCoverArt(URL.createObjectURL(imageBlob));
      });
    }
  }, [coverArtUrl]);

  const downloadImage = async (url) => {
    const response = await fetch(url);
    const imageBlob = await response.blob();
    return imageBlob;
  };

  const handleSongClick = async (songTitle) => {
    setLoading(true);

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
    }
  };

  const sortedLyrics = lyrics ? Object.entries(lyrics).sort(([aIndex], [bIndex]) => aIndex - bIndex) : [];

  return (
    <div className="container">
      <div className="content">
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
        {loading && <LoadingIcon loading={loading} />}
        {coverArt && <img src={coverArt} alt="Album Cover" className="album-cover" />} {/* Display downloaded cover art */}
        {scores && <ScoreBars scores={scores} />}
        
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

        {selectedSong && topics[selectedSong] && (
          <div className="topics-section">
            <h2>Topics for {selectedSong}</h2>
            <ul>
              {topics[selectedSong].split('\n').map((topic, index) => (
                <li key={index}>{topic}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
