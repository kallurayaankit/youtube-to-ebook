import yt_dlp
import time
import requests
import re
import os

def get_transcript(video_id):
    """
    Downloads English auto-generated subtitles using yt-dlp (info dict)
    and the direct subtitle URL. Falls back to downloading the VTT file
    via yt-dlp if no direct URL is found.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        # Step 1 – get video info (includes subtitle URLs)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        # Step 2 – find English automatic captions
        subs = info.get('automatic_captions') or info.get('subtitles') or {}
        eng_subs = subs.get('en')
        if not eng_subs:
            print(f"    No English subtitles found for {video_id}")
            return None
        
        # Pick the first available VTT URL
        sub_url = None
        for fmt in eng_subs:
            if fmt.get('ext') in ['vtt', 'srv1', 'srv2', 'srv3', 'json3']:
                sub_url = fmt.get('url')
                break
        
        vtt_text = None
        
        if sub_url:
            # Try to download the VTT content directly
            resp = requests.get(sub_url)
            if resp.status_code == 200:
                vtt_text = resp.text
            else:
                print(f"    Failed to download subtitle file (HTTP {resp.status_code})")
        
        # If direct URL failed, fallback: let yt-dlp write the file
        if not vtt_text:
            print("    Falling back to yt-dlp subtitle download...")
            # Temporarily change output template to capture subtitles
            ydl.params['outtmpl'] = f'{video_id}.%(ext)s'
            ydl.params['quiet'] = False
            ydl.download([url])
            vtt_file = None
            for f in os.listdir('.'):
                if f.startswith(video_id) and f.endswith('.en.vtt'):
                    vtt_file = f
                    break
            if vtt_file:
                with open(vtt_file, 'r', encoding='utf-8') as f:
                    vtt_text = f.read()
                os.remove(vtt_file)
            else:
                print("    Could not find downloaded subtitle file.")
                return None
        
        # Step 3 – parse VTT to plain text
        lines = []
        for line in vtt_text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith(('WEBVTT', 'Kind:', 'Language:')) or '-->' in line:
                continue
            # Remove HTML tags
            clean = re.sub(r'<[^>]+>', '', line)
            if clean:
                lines.append(clean)
        
        return ' '.join(lines) if lines else None
    
    except Exception as e:
        print(f"    Could not fetch transcript for {video_id}: {e}")
        return None
    finally:
        time.sleep(2)   # Be polite to YouTube