import json
import os

TRACKER_FILE = "processed_videos.json"

def load_processed():
    if not os.path.exists(TRACKER_FILE):
        return set()
    with open(TRACKER_FILE, 'r') as f:
        return set(json.load(f))

def save_processed(video_id):
    processed = load_processed()
    processed.add(video_id)
    with open(TRACKER_FILE, 'w') as f:
        json.dump(list(processed), f)