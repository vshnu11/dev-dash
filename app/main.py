import streamlit as st
import github_handler as gh

if __name__ == "__main__":
    st.title("🔧 DevDash - GitHub Commit Viewer")

    # Sidebar
    # st.sidebar.title("DevDash")

    user_name = st.text_input("Enter your GitHub username")
    # submit = st.button("Submit")

    if user_name:
        gh.get_overview(user_name)

        # choice = st.radio("Do you want to see more details of any repository?", ["Yes", "No"], index=None)
        repo_name = st.text_input("Enter a repository name if you want to see more details:")
        
        if repo_name:
            with st.spinner("🔄 Fetching repository data..."):
                try:
                    gh.fetch_commits(repo_name, user_name)
                except Exception as e:
                    st.error(f"❌ Error: {e}")    