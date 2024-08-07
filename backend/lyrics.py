import lyricsgenius
import json
import re
import google.generativeai as genai
import string
import time

GENIUS_ACCESS_TOKEN = '1CIpfBy4yJZqfQ-GeEGAf2chHIbqnhIrzZ31H5aE25NL89LDDttBgLbHA9yKiutP'
GENAI_API_KEY = 'AIzaSyA4k6mW9mtJofq1QMA5EKmeX_R8oDizQuM'

def filter_lyrics(lyrics):
    lines = lyrics.split('\n')
    filtered_lines = [line for line in lines if ']' not in line]
    filtered_lines = [re.sub(r'.{2}Embed', '', line) for line in filtered_lines]
    return '\n'.join(filtered_lines)

def fetch_album_tracks_and_lyrics(query, retries=3, timeout=10):
    api = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, timeout=timeout)

    # Split the input query into album name and artist name
    try:
        album_name, artist_name = query.split(' by ')
    except ValueError:
        raise ValueError("Query should be in the format '[album name] by [artist name]'")

    for attempt in range(retries):
        try:
            search_result = api.search_album(album_name, artist=artist_name, text_format=True)
            
            # Ensure the search result is valid
            if not search_result:
                raise Exception("No search result returned from Genius API")

            search_result.save_lyrics("lyrics.json", overwrite=True)
            with open("lyrics.json", 'r') as f:
                data = json.load(f)

            # Check the structure of data
            if "tracks" not in data or not isinstance(data["tracks"], list):
                raise Exception("Invalid data format: 'tracks' key not found or not a list")

            numtracks = len(data["tracks"])
            if numtracks == 0:
                raise Exception("No tracks found in the album")

            lyrics_dict = {}

            for i in range(numtracks):
                if "song" not in data["tracks"][i] or "lyrics" not in data["tracks"][i]["song"]:
                    raise Exception(f"Invalid track format at index {i}")
                lyrics = filter_lyrics(data["tracks"][i]["song"]["lyrics"])
                key = str(i + 1)  # Use numbers for keys
                lyrics_dict[key] = {
                    'title': data["tracks"][i]["song"]["title"],
                    'lyrics': lyrics
                }

            with open("lyrics.json", 'w') as f:
                json.dump(lyrics_dict, f, indent=4)

            with open("lyrics.txt", 'w') as f:
                for key, info in lyrics_dict.items():
                    title = info['title']
                    lyrics = info['lyrics']
                    f.write(f"{title}\n{lyrics}\n\n")

            album_title = search_result.full_title
            return lyrics_dict, album_title

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(2)  # Optional: wait for a few seconds before retrying
            else:
                print("All attempts failed.")
                raise e


def get_song_topic(lyrics, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"in only three words, give the themes discussed in the lyrics: {lyrics}"
        response = model.generate_content(prompt)
        print(response)
        if response and hasattr(response, 'text'):
            return response.text
        else:
            print(f"API key {api_key} returned an invalid response.")
        
    except Exception as e:
        print(f"Error with API key {api_key}: {e}")
    
    return "Song contains questionable lyrics for Gemini to parse"
