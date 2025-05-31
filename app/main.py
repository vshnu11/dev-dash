import streamlit as st
from github import Github
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

g = Github(GITHUB_TOKEN)

st.title("🔧 DevDash - GitHub Commit Viewer")

repo_name = st.text_input("Enter a repository (e.g. torvalds/linux):")

if repo_name:
    try:
        # Fetch repo
        repo = g.get_repo(repo_name)

        # Get latest 100 commits
        commits = repo.get_commits()[:100]

        st.subheader(f"Latest commits for {repo_name}")
        for commit in commits:
            author = commit.commit.author.name
            message = commit.commit.message
            date = commit.commit.author.date.strftime("%d-%m-%Y %H:%M:%S")
            st.markdown(f"- **{author}**: {message} \n⌚ {date}")

        # Commit activity chart
        dates = [commit.commit.author.date.date() for commit in commits]
        df = pd.DataFrame(dates, columns=["date"])
        commit_counts = df["date"].value_counts().sort_index()

        st.subheader("📈 Commit Activity (Last 100 Commits)")
        st.bar_chart(commit_counts)

    except Exception as e:
        st.error(f"Error: {str(e)}")        
