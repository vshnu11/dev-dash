import streamlit as st
from github import Github
import os
from dotenv import load_dotenv
import pandas as pd
from collections import Counter
from collections import defaultdict

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

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

def fetch_commits(repo_name, user_name):
    if repo_name:
        try:
            repo_name = f"{user_name}/{repo_name}"
            # Fetch repo
            repo = g.get_repo(repo_name)

            # Get latest 25 commits
            commits = repo.get_commits()[:25]

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

            st.subheader("📈 Commit Activity (Last 25 Commits)")
            st.bar_chart(commit_counts)

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
            # st.dataframe(author_df.reset_index(drop=True))

        except Exception as e:
            st.error(f"Error: {str(e)}")  