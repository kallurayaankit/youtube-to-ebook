import ollama

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
    response = ollama.chat(
        model='llama3.2:3b',
        messages=[
            {"role": "system", "content": "You are a professional editor specializing in transforming video content into engaging written articles."},
            {"role": "user", "content": prompt}
        ],
        options={'temperature': 0.7, 'num_predict': 4096}
    )
    return response['message']['content']