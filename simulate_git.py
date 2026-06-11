import os
import subprocess
import requests
import shutil
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
PROJECT_NAME = "test_repo_sim_123"

print("=== MEMULAI SIMULASI GIT PUSH LOKAL ===")
url = "https://api.github.com/user/repos"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
data = {"name": PROJECT_NAME, "private": False}

print(f"1. Membangun Repo di GitHub API: {PROJECT_NAME}...")
r = requests.post(url, headers=headers, json=data)
if r.status_code in [201, 422]:
    print(f"   -> Berhasil (Status {r.status_code})")
else:
    print(f"   -> Gagal membuat repo: {r.status_code} {r.text}")

repo_url_auth = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{PROJECT_NAME}.git"

if os.path.exists(PROJECT_NAME):
    shutil.rmtree(PROJECT_NAME)
os.makedirs(PROJECT_NAME, exist_ok=True)

with open(os.path.join(PROJECT_NAME, "test.txt"), "w") as f:
    f.write("Simulasi berhasil membuktikan push jalan.")

commands = [
    "git init",
    "git config user.email \"vps-agent@ai.local\"",
    "git config user.name \"Immortal Qwen Agent\"",
    "git add .",
    "git commit -m \"Test simulasi\" --allow-empty",
    "git branch -M main",
    "git remote remove origin",
    f"git remote add origin {repo_url_auth}",
    "git push -u origin main -f"
]

print("\n2. Menjalankan Commands Git...")
for cmd in commands:
    safe_cmd = cmd.replace(GITHUB_TOKEN, "***TOKEN***")
    print(f"\n[Execute]: {safe_cmd}")
    
    result = subprocess.run(cmd, shell=True, cwd=PROJECT_NAME, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"  [stdout]: {result.stdout.strip()}")
    if result.stderr.strip():
        print(f"  [stderr]: {result.stderr.strip()}")

print("\n=== SIMULASI SELESAI ===")
