import os
from dotenv import load_dotenv

# Try loading .env locally (has no effect in cloud)
load_dotenv()

# In Streamlit Cloud, secrets are in st.secrets, but for plain Python scripts
# we can use os.getenv and then later override in the web app.
def get_secret(key):
    return os.getenv(key)