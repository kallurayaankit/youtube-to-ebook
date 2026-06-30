import os
import datetime
from dotenv import load_dotenv
from get_videos import get_latest_videos
from get_transcripts import get_transcript
from write_articles import write_article
from send_email import create_epub, send_email
from video_tracker import load_processed, save_processed

load_dotenv()

def main():
    # Read channels from file
    if not os.path.exists("channels.txt"):
        print("channels.txt not found. Add at least one YouTube handle.")
        return
    
    with open("channels.txt", "r") as f:
        channels = [line.strip() for line in f if line.strip()]
    
    all_articles = []
    for channel in channels:
        print(f"Processing channel: {channel}")
        try:
            videos = get_latest_videos(channel, max_results=3)
        except Exception as e:
            print(f"Error fetching videos for {channel}: {e}")
            continue
        
        processed_set = load_processed()
        for video in videos:
            vid = video["video_id"]
            if vid in processed_set:
                print(f"  Skipping {video['title']} (already processed)")
                continue
            
            print(f"  Getting transcript for: {video['title']}")
            transcript = get_transcript(vid)
            if not transcript:
                print(f"    No transcript found, skipping.")
                continue
            
            print(f"  Writing article with DeepSeek...")
            article_text = write_article(video["title"], video["description"], transcript)
            
            all_articles.append({
                "title": video["title"],
                "content": article_text
            })
            save_processed(vid)
    
    if not all_articles:
        print("No new articles to package.")
        return
    
    # Create ebook
    today_str = datetime.date.today().isoformat()
    epub_path = f"newsletters/ebook_{today_str}.epub"
    os.makedirs("newsletters", exist_ok=True)
    create_epub("Weekly YouTube Digest", all_articles, epub_path)
    print(f"Ebook created: {epub_path}")
    
    # Send email
    recipient = os.getenv("EMAIL_USER")
    send_email(recipient, f"Your Weekly YouTube Ebook – {today_str}", epub_path)

if __name__ == "__main__":
    main()