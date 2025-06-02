import streamlit as st
from github import Github
import os
from dotenv import load_dotenv
import pandas as pd
from collections import defaultdict

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

def get_overview(user_name):
    if user_name:
        st.subheader(f"🙎‍♂️ Profile Overview of @{user_name}")
        user = g.get_user(user_name)
        st.image(user.avatar_url, width=100)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🧑 Name", user_name)
        col2.metric("📌 Public repos", user.public_repos)
        col3.metric("🙎‍♂️🙎‍♂️ Followers", user.followers)
        col4.metric("🙎‍♀️🙎‍♀️ Following", user.following)
        st.markdown("---")
        return
    
def get_repos(user_name):
    user = g.get_user(user_name)
    repo_list = [repo.full_name for repo in user.get_repos()]
    if not repo_list:
        found = False
    else:
        found = True
    return found, repo_list    

def fetch_commits(repo_name):
    if repo_name:
        # Fetch repo
        repo = g.get_repo(repo_name)

        # Get latest 25 commits
        commits = repo.get_commits()[:25]

        st.subheader(f"📦 Recent commits for {repo_name}")
        for commit in commits:
            author = commit.commit.author.name
            message = commit.commit.message
            date = commit.commit.author.date.strftime("%d-%m-%Y %H:%M:%S")
            st.markdown(f"- **{author}**: {message} \n⌚ {date}")
        st.markdown("---")

        # Commit activity chart
        dates = [commit.commit.author.date.date() for commit in commits]
        df = pd.DataFrame(dates, columns=["date"])
        commit_counts = df["date"].value_counts().sort_index()

        st.subheader("📈 Commit Activity (Last 25 Commits)")
        st.bar_chart(commit_counts)
        st.markdown("---")

        # Count commits per contributor login
        author_counts = defaultdict(int)
        for commit in commits:
            if commit.author:
                login = commit.author.login
                author_counts[login] += 1

        # Build DataFrame with contributor links
        data = []
        for login, count in author_counts.items():
            profile_url = f"https://github.com/{login}"
            data.append((f"[{login}]({profile_url})", count))

        author_df = pd.DataFrame(data, columns=["Contributor", "Commits"])
        author_df = author_df.sort_values(by="Commits", ascending=False)

        # Show in Streamlit
        st.subheader("🙎‍♂️🙎‍♂️ Top Contributors (Last 25 Commits)")
        for index, row in author_df.iterrows():
            st.markdown(f"- {row['Contributor']} - **{row['Commits']}** commits")
        return