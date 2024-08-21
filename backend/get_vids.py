import requests
import json
import re

API_KEY = 'xx'
CHANNEL_ID = 'UCt7fwAhXDy3oNFTAzF2o8Pw'

PLAYLIST_IDS = {
    "Electronic Reviews": "PLP4CSgl7K7ormX2pL9h0inES2Ub630NoL",
    "Rock Reviews": "PLP4CSgl7K7ori6-Iz-AWcX561iWCfapt_",
    "Hip Hop Reviews": "PLP4CSgl7K7ormBIO138tYonB949PHnNcP",
    "Pop Reviews": "PLP4CSgl7K7oqibt_5oDPppWxQ0iaxyyeq",
    "Experimental": "PLP4CSgl7K7orSnEBkcBRqI5fDgKSs5c8o",
    "Classics": "PLP4CSgl7K7or_7JI7RsEsptyS4wfLFGIN",
    "Metal": "PLP4CSgl7K7orAG2zKtoJKnTt_bAnLwTXo"
}

def get_videos_in_playlist(playlist_id, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": api_key
    }
    videos = []
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Save the JSON response to a file
        with open(f'playlist_{playlist_id}.json', 'w') as f:
            json.dump(data, f, indent=4)
        if 'items' in data:
            videos.extend(data['items'])
        
        # Handle pagination
        while 'nextPageToken' in data:
            params['pageToken'] = data['nextPageToken']
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                # Save the JSON response to a file
                with open(f'playlist_{playlist_id}.json', 'a') as f:
                    json.dump(data, f, indent=4)
                if 'items' in data:
                    videos.extend(data['items'])  
            else:
                print(f"Error fetching more videos: {response.status_code}")
                break
    else:
        print(f"Error fetching videos: {response.status_code}")
    
    return videos

def add_to_txt_file(file_path, lines):
    try:
        with open(file_path, 'a') as f:
            for line in lines:
                f.write(f"{line}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def extract_artist_album(video_title):
    pattern = re.compile(r'(.+?) - (.+?) \[')
    match = pattern.search(video_title)
    if match:
        artist = match.group(1).strip()
        album = match.group(2).strip()
        return artist, album
    return None, None

def main():
    all_video_titles = []
    all_video_ids = []
    
    for title, playlist_id in PLAYLIST_IDS.items():
        videos = get_videos_in_playlist(playlist_id, API_KEY)
        for video in videos:
            video_title = video['snippet']['title']
            video_id = video['snippet']['resourceId']['videoId']
            all_video_titles.append(f"{video_title} ({video_id})")
            all_video_ids.append(video_id)
    
    titles_file_path = "video_titles.txt"
    add_to_txt_file(titles_file_path, all_video_titles)
    print(f"Added {len(all_video_titles)} video titles to {titles_file_path}")
    
    artist_album_pairs = []
    for video_title in all_video_titles:
        # Extract the artist and album from the video title (excluding the video ID)
        video_title_clean = re.sub(r'\s*\(.*?\)\s*$', '', video_title)
        artist, album = extract_artist_album(video_title_clean)
        if artist and album:
            # Extract the video ID from the video title
            video_id = re.search(r'\((.*?)\)', video_title).group(1)
            artist_album_pairs.append((artist, album, video_id))
    
    albums_file_path = "albums.txt"
    add_to_txt_file(albums_file_path, [f"{artist} - {album} ({video_id})" for artist, album, video_id in artist_album_pairs])
    print(f"Added {len(artist_album_pairs)} artist/album pairs to {albums_file_path}")

if __name__ == "__main__":
    main()
