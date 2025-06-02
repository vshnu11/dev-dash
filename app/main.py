import streamlit as st
import github_handler as gh
import github.GithubException as GithubException

def main():
    st.title("🚀 ObserGit - GitHub Activity Dashboard")
    user_name = st.text_input("Enter your GitHub username")

    if user_name:
        try:
            gh.get_overview(user_name)
            found, repos = gh.get_repos(user_name)

            if found:
                selected_repo = st.selectbox("📂 Choose a repository", repos)
                if selected_repo:
                    with st.spinner("🔄 Fetching repository data..."):
                        commits = gh.fetch_commits(selected_repo)
                        gh.generate_activity_chart(commits)
                        gh.get_top_contributors(commits)
            else:
                st.info(f"⚠ No public repositories found for @{user_name}") 

        except GithubException as ge:
            st.error(f"❗ GitHub API Error: {ge.status} - {ge.data.get('message', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    main()