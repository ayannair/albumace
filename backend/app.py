from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
from db import get_db
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

app = Flask(__name__)
CORS(app)

GENAI_API_KEY = 'AIzaSyBlH_IUdgUmfxM7ejUeRZpFTExCCvEf8oQ'

db = get_db()
collection = db.get_collection('albums')


@app.route('/search')
def search():
    query = request.args.get('query')
    
    try:
        # Check if query is in the DB
        db_result = collection.find_one({'title': {'$regex': query, '$options': 'i'}})
        
        if db_result:
            # Convert ObjectId to string if present
            if '_id' in db_result:
                db_result['_id'] = str(db_result['_id'])

            # Debugging: Print the result to verify
            print("DB Result:", db_result)

            # Write to results.json
            with open('results.json', 'w') as f:
                json.dump(db_result, f, indent=4)
            
            # Debugging: Check if the file was written successfully
            print("Updated results.json")

            return jsonify(db_result)
        else:
            return jsonify({'error': 'No results found'})

    except Exception as e:
        # Debugging: Print any exceptions
        print("Error: ", str(e))
        return jsonify({'error': str(e)})
    

def get_song_topic(lyrics, api_key):
    try:
        # Configure the Google Gemini API with the single API key
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prepare the prompt with the provided lyrics
        prompt = f"In only three words, give the themes discussed in the lyrics: {lyrics}"
        
        # Generate content with safety settings
        response = model.generate_content(
            prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
            }
        )
        
        # Check and return the response text
        if response and hasattr(response, 'text'):
            return response.text
        else:
            print(f"API key {api_key} returned an invalid response.")
            return "Song contains inappropriate lyrics"
    except Exception as e:
        print(f"Error with API key {api_key}: {e}")
        return "An error occurred with the API key"

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
                topic = get_song_topic(lyrics, GENAI_API_KEY)
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
            # Update the `cards` field with the new scores
            cards_updates = {}
            percentiles = {}
            
            for score_field, card_field in score_to_card.items():
                if score_field in input_scores:
                    # Get the existing array or initialize an empty list
                    existing_scores = entry.get('cards', {}).get(card_field, [])
                    existing_scores.append(input_scores[score_field])
                    existing_scores.sort()
                    cards_updates[f'cards.{card_field}'] = existing_scores
                    position = existing_scores.index(input_scores[score_field])+1
                    percentile = (position / len(existing_scores)) * 100
                    percentiles[score_field] = percentile
            
            if cards_updates:
                collection.update_one({'_id': entry['_id']}, {'$set': {'score': updated_scores, 'total_inputs': updated_total_inputs, **cards_updates}})

            print(f"Updated scores for {title} (found in database): {input_scores}")
            return jsonify({'message': 'Scores updated successfully (found in database)', 'updated_scores': updated_scores, 'percentiles': percentiles})
        else:
            print(f"Error: No matching entry found for {title}")
            return jsonify({'error': 'No matching entry found for the provided title'}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred'}), 500
    
@app.route('/top_bottom_albums', methods=['GET'])
def get_top_bottom_albums():
    score_type = request.args.get('score_type')

    if not score_type:
        return jsonify({"error": "Score type is required"}), 400

    try:
        top_albums = list(collection.find().sort(f"score.{score_type}", -1).limit(5))
        bottom_albums = list(collection.find().sort(f"score.{score_type}", 1).limit(5))

        top_albums_data = [
            {
                "album_name": album["title"], 
                "score": round(album["score"].get(score_type), 1) if album["score"].get(score_type) is not None else None
            } 
            for album in top_albums
        ]

        bottom_albums_data = [
            {
                "album_name": album["title"], 
                "score": round(album["score"].get(score_type), 1) if album["score"].get(score_type) is not None else None
            } 
            for album in bottom_albums
        ]

        return jsonify({"top_albums": top_albums_data, "bottom_albums": bottom_albums_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/top_popular_albums', methods=['GET'])
def get_top_popular_albums():
    try:
        # Retrieve the top 5 albums sorted by total_inputs in descending order
        popular_albums = list(collection.find().sort("total_inputs", -1).limit(5))

        popular_albums_data = [
            {
                "album_name": album["title"], 
                "total_inputs": album.get("total_inputs", 0)
            } 
            for album in popular_albums
        ]

        return jsonify({"popular_albums": popular_albums_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000,debug=True)