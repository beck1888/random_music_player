import json
import dotenv

# Read songs into a python dict
def get_songs():
    with open('songs.json', 'r') as f:
        songs_dict = dict(json.load(f))
        return songs_dict
    
# Add a song
def add_song(title, youtube_url):
    songs = get_songs() # Load songs file into dict
    songs[title] = youtube_url # Add song name and url to dict
    with open('songs.json', 'w') as f:
        json.dump(songs, f, indent=4) # Write back to json in a pretty format

# Remove a song
def remove_song(title):
    songs = get_songs() # Load songs file into dict
    del songs[title] # Remove song name and url from dict
    with open('songs.json', 'w') as f:
        json.dump(songs, f, indent=4)

# Check if the user add song password is right
def is_correct_password(user_password):
    if user_password == dotenv.get_key('.env', 'ADD_SONG_PASSWORD'): # Compare user input directly to the function getting the key
        return True
    else:
        return False