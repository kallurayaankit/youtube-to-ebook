# YouTube Channel → Ebook 📚

Turn any YouTube channel into a polished, magazine-style ebook with AI.  
Built with Streamlit, yt-dlp, and DeepSeek.

## How it works
1. Enter a YouTube channel handle (e.g., @mkbhd)
2. We fetch the latest non‑Short videos and their transcripts
3. An AI (DeepSeek) rewrites each transcript into a beautifully structured article
4. All articles are bundled into an EPUB and sent to your email

## Tech Stack
- Python, Streamlit (web UI)
- YouTube Data API v3 (video fetching)
- yt-dlp (transcript extraction)
- DeepSeek API (AI rewriting)
- ebooklib (EPUB generation)
- Gmail SMTP (delivery)

## Run locally
\`\`\`bash
git clone https://github.com/yourusername/youtube-to-ebook.git
cd youtube-to-ebook
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
\`\`\`

## Environment variables
Create a `.env` file with:
- YOUTUBE_API_KEY
- DEEPSEEK_API_KEY
- EMAIL_USER
- EMAIL_PASSWORD

(Or use Streamlit Secrets when deploying to Streamlit Cloud)