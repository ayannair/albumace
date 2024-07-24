from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import yt_dlp
import whisper
from run import run_notebook
import json

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = 'API_KEY'
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
        model = whisper.load_model("base")
        print("loading model...")
        result = model.transcribe(audio_file, fp16=False)
        print("transcribed audio")
        transcription_text = result["text"]

        with open(f'transcript.txt', "w") as f:
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
            notebook_path = '/Users/ayannair/Documents/projects/fantanosize/backend/analysis.ipynb'
            result = run_notebook(notebook_path)
            output_json_path = '/Users/ayannair/Documents/projects/fantanosize/backend/results.json'
            with open(output_json_path) as json_file:
                score = json.load(json_file)
                print(score)
            
            return jsonify({'link': youtube_link, 'score': score})
            
        return jsonify({'link': youtube_link})
    
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
