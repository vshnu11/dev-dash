import asyncio
import streamlit as st
from github import Github
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

g = Github(GITHUB_TOKEN)

def fetch_commits(repo_name, user_name):
    if repo_name:
        try:
            repo_name = f"{user_name}/{repo_name}"
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

def get_overview(user_name):
    if user_name:
        st.subheader(f"Developer Dashboard for @{user_name}")
        try:
            user = g.get_user(user_name)
            st.subheader("🙍‍♂️ Basic Info")
            st.write(f"Name: {user_name}")
            st.write(f"Public repos: {user.public_repos}")
            st.write(f"Followers: {user.followers}")
            st.write(f"Following: {user.following}")
        except:
            st.error("Failed to fetch user info. Check username or token.") 
    

if __name__ == "__main__":
    st.title("🔧 DevDash - GitHub Commit Viewer")

    # Sidebar
    # st.sidebar.title("DevDash")

    user_name = st.text_input("Enter your GitHub username")
    # submit = st.button("Submit")

    if user_name:
        get_overview(user_name)

        # choice = st.radio("Do you want to see more details of any repository?", ["Yes", "No"], index=None)
        repo_name = st.text_input("Enter a repository name if you want to see more details:")
        
        if repo_name:
            fetch_commits(repo_name, user_name)