from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import yt_dlp
import whisper
import json
from analysis import analyze_text_file
from lyrics import fetch_album_tracks_and_lyrics, get_song_topic, GENAI_API_KEYS
from db import get_db
from bson import ObjectId

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = 'xx'
FFMPEG_PATH = '/opt/homebrew/bin/ffmpeg'

db = get_db()
collection = db.get_collection('albums')

# deletes genius translations
def cleanup_translations():
    try:
        pattern = r'.* by Genius .*'
        result = collection.delete_many({'title': {'$regex': pattern, '$options': 'i'}})
        print(f"Deleted {result.deleted_count} entries with translations.")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

# gets audio from youtube
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

# uses openai whisper to transcribe audio
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
        # check if query is in db
        db_result = collection.find_one({'title': {'$regex': query, '$options': 'i'}})
        
        if db_result:
            db_result['_id'] = str(db_result['_id'])
            with open('results.json', 'w') as f:
                json.dump(db_result, f, indent=4)
            return jsonify(db_result)

        # if not in db, get from youtube
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
            
            scores = analyze_text_file('transcript.txt')

            lyrics, title = fetch_album_tracks_and_lyrics(query)

            results = {
                'title': title,
                'score': scores,
                'lyrics': lyrics,
                'total_inputs': 1
            }
            
            # insert/update db
            collection.update_one(
                {'title': title},
                {'$set': results},
                upsert=True
            )

            cleanup_translations()

            with open('results.json', 'w') as f:
                json.dump(results, f, indent=4)

            return jsonify(results)
            
        return jsonify({'link': youtube_link})
    
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_topic')
def get_topic():
    song_title = request.args.get('song_title')
    lyrics_dict_path = 'results.json'

    try:
        # first find in db
        album_data = collection.find_one({
            'lyrics': {'$elemMatch': {'title': song_title}}
        })

        if album_data:
            # write to results json file
            with open(lyrics_dict_path, 'w') as f:
                json.dump(album_data, f, indent=4)
        
        with open(lyrics_dict_path, 'r') as f:
            lyrics_dict = json.load(f)

        # find song by title
        song_entry = next((item for key, item in lyrics_dict.get('lyrics', {}).items() if item['title'] == song_title), None)

        if song_entry:
            if(song_entry['topics'] != 'empty'):
                print("found in db: ", song_entry['topics'])
                return jsonify({'topic': song_entry['topics']})   
            else:
                lyrics = song_entry['lyrics']
                topic = get_song_topic(lyrics, GENAI_API_KEYS)
                if(song_entry['topics'] == 'empty'):
                    song_entry['topics'] = topic
                    print("added to db: ", song_entry['topics'])
                return jsonify({'topic': topic})
        else:
            return jsonify({'error': 'Song title not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])

    # case insensitive search
    results = collection.find({
        'title': {'$regex': query, '$options': 'i'}
    })

    suggestions = [result['title'] for result in results]
    return jsonify(suggestions)

# updates database from custom album card
# need to do: total_inputs by user instead of incrementing every time same user edits/save card
def update_scores_in_database(entry_id, current_scores, input_scores, total_inputs):
    updated_scores = {}
    for key in current_scores:
        updated_scores[key] = (current_scores[key] * total_inputs + input_scores.get(key, 0)) / (total_inputs + 1)
    
    updated_total_inputs = total_inputs + 1

    collection.update_one(
        {'_id': entry_id},
        {'$set': {'score': updated_scores, 'total_inputs': updated_total_inputs}}
    )
    return updated_scores, updated_total_inputs

@app.route('/save_scores', methods=['POST'])
def save_scores():
    score_to_card = {
        'lyrics_score': 'lyrics_scores',
        'production_score': 'production_scores',
        'features_score': 'features_scores',
        'vocals_score': 'vocals_scores',
        'originality_score': 'originality_scores',
        'concept_score': 'concept_scores',
        'overall_score': 'overall_scores'
    }
    try:
        data = request.json
        title = data['title']
        input_scores = data['scores']
        entry = collection.find_one({'title': {'$regex': title, '$options': 'i'}})
        if entry:
            updated_scores, updated_total_inputs = update_scores_in_database(
                entry['_id'],
                entry.get('score', {}),
                input_scores,
                entry.get('total_inputs', 1)
            )

            # adds your card to a sorted array
            # working on providing percentile information on a user's submitted card
            cards_updates = {}
            
            for score_field, card_field in score_to_card.items():
                if score_field in input_scores:
                    existing_scores = entry.get('cards', {}).get(card_field, [])
                    existing_scores.append(input_scores[score_field])
                    existing_scores.sort()
                    cards_updates[f'cards.{card_field}'] = existing_scores
            
            if cards_updates:
                collection.update_one({'_id': entry['_id']}, {'$set': {'score': updated_scores, 'total_inputs': updated_total_inputs, **cards_updates}})

            print(f"Updated scores for {title} (found in database): {input_scores}")
            return jsonify({'message': 'Scores updated successfully (found in database)', 'updated_scores': updated_scores})
        else:
            print(f"Error: No matching entry found for {title}")
            return jsonify({'error': 'No matching entry found for the provided title'}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred'}), 500

    
if __name__ == '__main__':
    app.run(port=8000,debug=True)
