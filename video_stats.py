import requests
from requests.exceptions import ConnectionError,HTTPError,RequestException
import json
import os
import dotenv

dotenv.load_dotenv(dotenv_path="./.env") # Load environment variables from .env file

API_KEY = os.getenv("API_KEY")  # Get the API key from environment variables
channel_handle ="MrBeast" 

Max_Results = 50  # Maximum number of results to fetch per API call


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
        
    except RequestException as err:
        raise err
        
        
        

def get_video_ids(playlistid:str) -> list :
    
    playlist_items_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={Max_Results}&playlistId={playlistid}&key={API_KEY}"
    video_ids =[] # List to store video IDs
    pageToken = None # Token for pagination
    
    try:
        
        while True:
            url = playlist_items_url 
            if pageToken:   #
                url += f"&pageToken={pageToken}" # Append page token for pagination if available
             
            response = requests.get(url) 
            response.raise_for_status()
        
            print(response.status_code)
        
            data = response.json()
            with open("playlist_items.json","w") as file :
                json.dump(data,file,indent=4) # Write the JSON data to a file
            
            for item in data.get("items",[]): # if "items" exists, return it else return an empty list
                video_id = item["contentDetails"]["videoId"] # Extract video ID
                video_ids.append(video_id)
            
            pageToken = data.get("nextPageToken")
            
            
            if not pageToken:
                break
        
        
        return video_ids
        

    except RequestException as err:
        raise err
    

         
def extract_video_data(video_ids) :
    video_data = []
    
    # Function to batch video IDs into smaller lists
    def batch_list(video_id_list:list,batch_size:int) -> list:
     for video_id in range(0 , len(video_id_list),batch_size):
         yield video_id_list[video_id : video_id + batch_size]   # 

   
    try:
        
        for batch in batch_list(video_ids,50): #
            batch = ",".join(batch) # comma-separated IDs for the `id` parameter (string)
          
            url_video = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={batch}&key={API_KEY}"
            
            response = requests.get(url_video)
            response.raise_for_status()
            
            data = response.json()
            
            for item in data.get("items",[]): # if "items" exists, return it else return an empty list
                content = item.get("contentDetails",{})
                statistics = item.get("statistics",{})
                id= item["id"]
                snippet = item.get("snippet",{})
                
                record ={
                    "video_id" : id,
                    "title": snippet.get("title") ,
                    "publishedAt" : snippet.get("publishedAt"),
                    "duration": content.get("duration"),
                    "viewCount" : statistics.get("viewCount",None),
                    "likeCount": statistics.get("likeCount",None),
                    "CommentCount": statistics.get("commentCount",None) 
                    
                }
                
                
                video_data.append(record)
                
            
                
            
        return video_data
        
    except RequestException as err:
        raise err
    
    
    
    
    
if __name__ =="__main__": 
    playlistid = get_playlist_id(API_KEY=API_KEY,channel_handle=channel_handle)
    videolist= get_video_ids(playlistid)
    video_data = extract_video_data(video_ids=videolist)
    print(video_data)