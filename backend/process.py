import requests
import time

def process_albums():
    with open('albums.txt', 'r') as albums_file:
        albums = albums_file.readlines()

    for album in albums:
        album = album.strip()
        if not album:
            continue

        try:
            response = requests.get('http://127.0.0.1:5000/search', params={'query': album})
            response.raise_for_status()
            print(f"Processed album: {album}")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred for album {album}: {http_err}")
        except Exception as err:
            print(f"An error occurred for album {album}: {err}")
        
        # Sleep to avoid hitting rate limits
        time.sleep(2)

if __name__ == '__main__':
    process_albums()
