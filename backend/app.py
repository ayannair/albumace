from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import yt_dlp
import whisper
import json
from analysis import analyze_text_file
from lyrics import fetch_album_tracks_and_lyrics, get_song_topic, GENAI_API_KEYS

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = 'xx'
FFMPEG_PATH = '/opt/homebrew/bin/ffmpeg'

def download_audio(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'ffmpeg_location': FFMPEG_PATH,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return 'audio.wav'
    except Exception as e:
        raise Exception(f'Error downloading audio: {str(e)}')

def transcribe_audio(audio_file):
    try:
        model = whisper.load_model("tiny")
        print("Loading model...")
        result = model.transcribe(audio_file, fp16=False)
        print("Transcribed audio")
        transcription_text = result["text"]

        with open('transcript.txt', "w") as f:
            f.write(transcription_text)
        
        return transcription_text
    except Exception as e:
        raise Exception(f'Error transcribing audio: {str(e)}')

@app.route('/search')
def search():
    query = request.args.get('query')

    try:
        search_query = f'{query} TheNeedleDrop review'

        params = {
            'key': YOUTUBE_API_KEY,
            'part': 'snippet',
            'type': 'video',
            'maxResults': 1,
            'q': search_query
        }
        url = 'https://www.googleapis.com/youtube/v3/search'
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()

        video_id = data['items'][0]['id']['videoId']
        youtube_link = f'https://www.youtube.com/watch?v={video_id}'
        
        if youtube_link:
            audio = download_audio(youtube_link)
            transcribe_audio(audio)
            
            review_info_fp = 'review_info.txt'  # Ensure this path is correct for your setup
            scores = analyze_text_file('transcript.txt', review_info_fp)

            output_json_path = 'results.json'  # Ensure this path is correct for your setup
            
            lyrics, cover_art_url = fetch_album_tracks_and_lyrics(query)
            # cover_art_path = download_cover_art(cover_art_url)

            results = {
                'link': youtube_link,
                'score': scores,
                'lyrics': lyrics,
                'cover_art_url': cover_art_url
            }
            
            with open(output_json_path, 'w') as json_file:
                json.dump(results, json_file, indent=4)

            return jsonify(results)
            
        return jsonify({'link': youtube_link})
    
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_topic')
def get_topic():
    song_title = request.args.get('song_title')
    lyrics_dict_path = 'lyrics.json'

    try:
        with open(lyrics_dict_path, 'r') as f:
            lyrics_dict = json.load(f)

        # Log available keys for debugging
        print("Available song titles:", [v['title'] for v in lyrics_dict.values()])

        # Find the song entry based on the title
        song_entry = next((item for item in lyrics_dict.values() if item['title'] == song_title), None)

        if song_entry:
            lyrics = song_entry['lyrics']
            topic = get_song_topic(lyrics, GENAI_API_KEYS)
            return jsonify({'topic': topic})
        else:
            return jsonify({'error': 'Song title not found'})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
