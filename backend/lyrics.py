import lyricsgenius
import json
import requests
import re
import google.generativeai as genai

GENIUS_ACCESS_TOKEN = 'xx'

GENAI_API_KEYS = [
    'a',
    'b',
    'c'
]

def filter_lyrics(lyrics):
    lines = lyrics.split('\n')
    filtered_lines = [line for line in lines if ']' not in line]
    filtered_lines = [re.sub(r'.{2}Embed', '', line) for line in filtered_lines]
    return '\n'.join(filtered_lines)

def fetch_album_tracks_and_lyrics(album_name):
    api = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
    search_result = api.search_album(album_name, text_format=True)
    search_result.save_lyrics("lyrics.json", overwrite=True)
    with open("lyrics.json", 'r') as f:
        data = json.load(f)
    
    numtracks = len(data["tracks"])
    lyrics_dict = {}

    for i in range(numtracks):
        lyrics = filter_lyrics(data["tracks"][i]["song"]["lyrics"])
        lyrics_dict[i + 1] = {
            'title': data["tracks"][i]["song"]["title"],
            'lyrics': lyrics
        }
    
    with open("lyrics.json", 'w') as f:
        json.dump(lyrics_dict, f, indent=4)
    
    with open("lyrics.txt", 'w') as f:
        for index, info in lyrics_dict.items():
            title = info['title']
            lyrics = info['lyrics']
            f.write(f"{title}\n{lyrics}\n\n")
    
    # Save cover art URL
    cover_art_url = data["cover_art_thumbnail_url"]
    
    return lyrics_dict, cover_art_url

# def download_cover_art(cover_art_url, save_path='cover_art.jpg'):
#     response = requests.get(cover_art_url)
#     with open(save_path, 'wb') as f:
#         f.write(response.content)
#     return ''

def get_song_topic(lyrics, api_keys):
    for api_key in api_keys:
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
