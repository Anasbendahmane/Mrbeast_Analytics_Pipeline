import requests
from requests.exceptions import ConnectionError,HTTPError
import json
import os
import dotenv

dotenv.load_dotenv(dotenv_path="./.env") # Load environment variables from .env file

API_KEY = os.getenv("API_KEY")  # Get the API key from environment variables
channel_handle ="MrBeast" 


def get_playlist_id(API_KEY:str,channel_handle:str) -> str:
    
    
    try:

        url =f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}" # Construct the API URL

        response = requests.get(url) # Send GET request to the YouTube Data API
        
        response.raise_for_status()
        print(response.status_code)
        

        data = response.json() # Parse the JSON response

        with open("video_stats.json","w") as file :
            json.dump(data,file,indent=4) # Write the JSON data to a file


        playlist_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"] # Extract the uploads (playlist ID)
        print(playlist_id)
        
        return playlist_id
        
    except ConnectionError as conn_err:
        print(f"Connection Error ! {conn_err}")
        
        
        
if __name__ =="__main__": 
    get_playlist_id(API_KEY=API_KEY,channel_handle=channel_handle)