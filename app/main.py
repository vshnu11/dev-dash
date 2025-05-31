import streamlit as st
from github import Github
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(TOKEN)

st.set_page_config(page_title="DevDash", layout="wide")

# Sidebar
st.sidebar.title("DevDash")
username = st.sidebar.text_input("Enter your GitHub username", "your-username")

# Main area
st.title(f"Developer Dashboard for @{username}")

if username:
    try:
        user = g.get_user(username)
        st.subheader("🙍‍♂️ Basic Info")
        st.write(f"Name: {username}")
        st.write(f"Public repos: {user.public_repos}")
        st.write(f"Followers: {user.followers}")
        st.write(f"Following: {user.following}")
    except:
        st.error("Failed to fetch user info. Check username or token.") 

