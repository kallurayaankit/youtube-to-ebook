import streamlit as st
import datetime
import os
import re
from get_videos import get_latest_videos
from get_transcripts import get_transcript
from write_articles import write_article
from send_email import create_epub, send_email

st.set_page_config(page_title="YouTube → Ebook", page_icon="📚")
st.title("📚 YouTube Channel to Ebook")
st.markdown("Enter a YouTube channel **@handle** and your email. We'll turn their latest videos into a beautiful ebook and send it to you!")

# Input fields
handle = st.text_input("YouTube channel handle", placeholder="@mkbhd")
recipient_email = st.text_input("Your email address", placeholder="you@gmail.com")

# Validate email
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

if st.button("✨ Generate Ebook", type="primary"):
    if not handle:
        st.error("Please enter a YouTube handle (e.g., @mkbhd).")
    elif not recipient_email:
        st.error("Please enter your email address.")
    elif not is_valid_email(recipient_email):
        st.error("Please enter a valid email.")
    else:
        with st.spinner("Fetching latest videos..."):
            try:
                videos = get_latest_videos(handle, max_results=3)
            except Exception as e:
                st.error(f"Could not fetch videos for {handle}. Make sure the handle is correct and try again.")
                st.stop()

        if not videos:
            st.warning("No new non-Short videos found. Try again later!")
            st.stop()

        articles = []
        progress_bar = st.progress(0)
        for i, video in enumerate(videos):
            st.write(f"📝 Processing: **{video['title']}**")
            transcript = get_transcript(video["video_id"])
            if not transcript:
                st.write(f"⚠️ No transcript available, skipping.")
                continue

            st.write("🤖 Writing article...")
            article_text = write_article(video["title"], video["description"], transcript)
            articles.append({"title": video["title"], "content": article_text})
            progress_bar.progress((i + 1) / len(videos))

        if not articles:
            st.error("No articles could be created. Possibly no transcripts available.")
            st.stop()

        st.success(f"✅ {len(articles)} articles written!")

        # Create EPUB
        today_str = datetime.date.today().isoformat()
        epub_path = f"newsletters/ebook_{today_str}.epub"
        os.makedirs("newsletters", exist_ok=True)
        create_epub("YouTube Channel Digest", articles, epub_path)

        # Send email
        try:
            send_email(recipient_email, f"Your YouTube Ebook – {today_str}", epub_path)
            st.balloons()
            st.success(f"📬 Ebook sent to {recipient_email}!")
        except Exception as e:
            st.error(f"Could not send email: {e}")
            st.info("The ebook was generated but could not be sent. Please check the SMTP settings.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, yt‑dlp, and AI")