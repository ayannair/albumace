# AlbumAce

AlbumAce is an innovative social media platform for music lovers to share and explore album reviews. Designed with a focus on collaborative music critique, AlbumAce enables users to engage with reviews by Anthony Fantano and others, fostering a vibrant community centered around music discussion. The platform combines natural language processing (NLP) techniques with an intuitive user interface to bring album reviews to life.

## Features

- **User-Generated Reviews**: Share your thoughts on albums and rate them across categories like lyrics, production, originality, and more.
- **Comprehensive Sentiment Analysis**: Provides sentiment scores for album reviews across multiple dimensions, utilizing advanced NLP models like BERT and Google Gemini 1.5 Flash.
- **Dynamic Data Retrieval**: Fetches video reviews from YouTube and text reviews from various sources, including Anthony Fantano's TheNeedleDrop channel.
- **Topic Modeling**: Analyzes song lyrics using the Genius API to extract and model topics discussed in the album, adding depth to user reviews.
- **Engaging Social Platform**: Follow other users, comment on reviews, and build playlists based on shared album recommendations.
- **User Interface**: React-based frontend for an interactive and visually appealing experience. Explore reviews, topics, and album cover art in a clean, organized layout.
- **Backend Support**: Flask backend for efficient data handling, storage, and processing with MongoDB.

## Technologies Used

- **Frontend**: React, CSS
- **Backend**: Flask, Python
- **Database**: MongoDB
- **NLP Models**: BERT, Google Gemini 1.5 Flash
- **APIs**: YouTube Data API, Genius API, Google Gemini API
- **Transcription**: Whisper

## Installation and Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/albumace.git
    cd albumace
    ```

2. **Backend Setup**
    - Install the required Python packages:
      ```bash
      pip install -r backend/requirements.txt
      ```
    - Run the Flask server:
      ```bash
      cd backend
      flask run
      ```

3. **Frontend Setup**
    - Install the required Node packages:
      ```bash
      cd frontend
      npm install
      ```
    - Run the React app:
      ```bash
      npm start
      ```

4. **Environment Variables**
    - Create a `.env` file in the `backend` folder with the necessary API keys and configurations:
      ```env
      YOUTUBE_API_KEY=your_youtube_api_key
      GENIUS_API_KEY=your_genius_api_key
      GEMINI_API_KEYS=your_gemini_api_key
      ```

## Usage

1. Open the React app in your browser.
2. Sign up to create your profile and follow other users.
3. Search for an album review or write your own.
4. Rate the album across categories like lyrics, production, and originality.
5. Explore topics discussed in the lyrics using the Genius integration.
6. Engage with the community by commenting on reviews and sharing your thoughts on music.

## Contribute

We welcome contributions from the community! If you'd like to contribute to AlbumAce, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a detailed description of your changes.
