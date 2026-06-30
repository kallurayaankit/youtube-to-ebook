from ebooklib import epub
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

def create_epub(title, articles, output_path):
    book = epub.EpubBook()
    book.set_identifier('youtube-ebook')
    book.set_title(title)
    book.set_language('en')
    
    for i, article in enumerate(articles):
        chapter = epub.EpubHtml(
            title=article['title'],
            file_name=f'chapter_{i}.xhtml',
            lang='en'
        )
        content_html = f'<h1>{article["title"]}</h1>'
        for paragraph in article["content"].split('\n\n'):
            content_html += f'<p>{paragraph}</p>'
        chapter.content = content_html
        book.add_item(chapter)
    
    book.spine = ['nav'] + [f'chapter_{i}.xhtml' for i in range(len(articles))]
    epub.write_epub(output_path, book)

def send_email(recipient, subject, file_path):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    
    with open(file_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
        msg.attach(part)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
    print("Email sent successfully.")