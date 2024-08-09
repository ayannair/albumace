# Fantanosize

Fantanosize is an innovative project designed to analyze album reviews by Anthony Fantano, providing deeper insights into the music review process. This project employs advanced natural language processing (NLP) techniques, including BERT sentiment analysis models and Google Gemini 1.5 Flash, to deliver detailed sentiment scores for various aspects of an album.

## Features

- **Comprehensive Sentiment Analysis**: Breaks down reviews into specific categories such as lyrics, production, features, originality, concept, and vocals, providing sentiment scores for each.
- **Dynamic Data Retrieval**: Utilizes the YouTube Data API to fetch review videos from theneedledrop channel.
- **Text Processing**: Employs Whisper for transcribing video audio to text.
- **Topic Modeling**: Analyzes song lyrics using Genius and Gemini API to extract and model topics discussed in the album.
- **User Interface**: A React-based frontend that displays sentiment scores, topics, and album cover art in an organized and visually appealing manner.
- **Backend Support**: Flask backend to handle data retrieval, processing, and storage using MongoDB.

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
    git clone https://github.com/yourusername/fantanosize.git
    cd fantanosize
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
      GEMINI_API_KEYS = [
          your_gemini_api_keys
      ]
      ```

## Usage

1. Open the React app in your browser.
2. Search for an album review by entering the album name in the search bar.
3. View the sentiment scores for different aspects of the album.
4. Explore detailed topics discussed in the lyrics by clicking on individual songs.



Go deeper than a light to decent 7
