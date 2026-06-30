import os
from dotenv import load_dotenv

# Load .env file if it exists (local use)
load_dotenv()

from openai import OpenAI

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("Missing DEEPSEEK_API_KEY environment variable")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def write_article(video_title, video_description, transcript):
    prompt = f"""
You are a senior technology journalist. Rewrite the following raw YouTube transcript into a high-quality, magazine-style article.

Video Title: {video_title}
Video Description: {video_description}

Requirements:
1. Start with a compelling hook/introduction.
2. Structure the content with clear, logical paragraphs.
3. Fix typos, grammatical errors, and correct proper nouns (refer to the title/description).
4. Preserve the original speaker's tone and key insights.
5. Target length: 800–1200 words.

Raw Transcript:
{transcript}

Output only the final article text, with no additional commentary.
"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a professional editor specializing in transforming video content into engaging written articles."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        temperature=0.7
    )
    return response.choices[0].message.content