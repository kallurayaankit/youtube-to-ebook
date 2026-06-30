from googleapiclient.discovery import build
import os
import requests
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_channel_uploads_playlist_id(youtube, handle):
    request = youtube.channels().list(part="contentDetails", forHandle=handle)
    response = request.execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def is_youtube_short(video_id):
    shorts_url = f"https://www.youtube.com/shorts/{video_id}"
    try:
        response = requests.head(shorts_url, allow_redirects=True, timeout=5)
        return "/shorts/" in response.url
    except:
        return False

def get_latest_videos(handle, max_results=5):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    playlist_id = get_channel_uploads_playlist_id(youtube, handle)
    
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=max_results
    )
    response = request.execute()
    
    videos = []
    for item in response["items"]:
        video_id = item["snippet"]["resourceId"]["videoId"]
        if not is_youtube_short(video_id):
            videos.append({
                "video_id": video_id,
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "published_at": item["snippet"]["publishedAt"]
            })
    return videos