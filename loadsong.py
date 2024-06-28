import json
import os

def load_song(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The song file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        song_data = json.load(file)
    
    return song_data