import streamlit as st
import github_handler as gh
import github.GithubException as GithubException

def main():
    st.title("🚀 DevDash - GitHub Activity Dashboard")
    user_name = st.text_input("Enter your GitHub username")

    if user_name:
        try:
            gh.get_overview(user_name)
            repo_name = st.text_input("Enter a repository name if you want to see more details:")
            
            if repo_name:
                with st.spinner("🔄 Fetching repository data..."):
                    gh.fetch_commits(repo_name, user_name)
                            
        except GithubException as ge:
            st.error(f"❗ GitHub API Error: {ge.status} - {ge.data.get('message', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    main()