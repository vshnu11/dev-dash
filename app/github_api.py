import os
from dotenv import load_dotenv
import requests

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "vshnu11"

def get_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_recent_commits(repo_name, count=5):
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/commits"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if len(data) > count:
        return data[:count]
    else:
        return data
    
def get_repo_stats(repo_name):
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return {
        "name": data["name"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "language": data["language"],
        "open_issues": data["open_issues_count"]
    }

if __name__ == "__main__":
    repos = get_repos()
    for repo in repos[:3]:
        name = repo["name"]
        print(f"\n* Repo: {name}")
        stats = get_repo_stats(name)
        print(stats)
        commits = get_recent_commits(name)
        print(f"* Recent commits:")
        if isinstance(commits, list):
            for commit in commits: 
                    print(f"- {commit['commit']['message']}")
        else:
            print(commits.get('message'))         
