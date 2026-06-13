import os
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "ghp_isi-github-token-anda-disini")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "username_anda")

class GitManager:
    @staticmethod
    def commit(project_path, message):
        commands = [
            "git add .",
            f'git commit -m "{message}"'
        ]
        for cmd in commands:
            subprocess.run(cmd, shell=True, cwd=str(project_path), capture_output=True)

    @staticmethod
    def push(project_path):
        print("  [Mengunggah komit terbaru ke GitHub...]")
        subprocess.run("git push -u origin main -f", shell=True, cwd=str(project_path), capture_output=True)

    @staticmethod
    def create_repo(idea):
        print(f"  [+] Membuat repositori GitHub: {idea.get('project_name')}...")
        if not GITHUB_TOKEN or GITHUB_TOKEN == "ghp_isi-github-token-anda-disini":
            print("  [!] Token GitHub belum disetel. Melewati pembuatan repo.")
            return None

        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "name": idea.get('project_name'),
            "description": idea.get('description'),
            "private": False
        }
        
        try:
            r = requests.post(url, headers=headers, json=data)
            response_data = r.json()
            if "owner" in response_data:
                actual_username = response_data["owner"]["login"]
            else:
                user_req = requests.get("https://api.github.com/user", headers=headers)
                actual_username = user_req.json().get("login", GITHUB_USERNAME)
                
            repo_url_auth = f"https://{GITHUB_TOKEN}@github.com/{actual_username}/{idea.get('project_name')}.git"
            repo_url_clean = f"https://github.com/{actual_username}/{idea.get('project_name')}.git"
            return repo_url_auth, repo_url_clean
        except Exception as e:
            print(f"  [!] Gagal membuat repo: {e}")
            return None

    @staticmethod
    def initialize_repo(project_path, repo_urls):
        subprocess.run("git init", shell=True, cwd=str(project_path), capture_output=True)
        subprocess.run("git config user.email \"vps-agent@ai.local\"", shell=True, cwd=str(project_path), capture_output=True)
        subprocess.run("git config user.name \"Dedicated SaaS Engineer\"", shell=True, cwd=str(project_path), capture_output=True)
        subprocess.run("git branch -M main", shell=True, cwd=str(project_path), capture_output=True)
        
        if repo_urls:
            repo_url_auth, repo_url_clean = repo_urls
            subprocess.run("git remote remove origin", shell=True, cwd=str(project_path), capture_output=True)
            subprocess.run(f"git remote add origin {repo_url_auth}", shell=True, cwd=str(project_path), capture_output=True)
            return repo_url_clean
        return None
