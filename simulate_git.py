import os
import subprocess
import requests
import shutil
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# Kita pura-pura username di env itu salah (typo)
GITHUB_USERNAME_DI_ENV = "ini_username_typo_ngawur"
PROJECT_NAME = "super_test_repo_12345"

print("=== MEMULAI SUPER SIMULASI GIT PUSH ===")
url = "https://api.github.com/user/repos"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
data = {"name": PROJECT_NAME, "private": False}

print(f"1. Membangun Repo di GitHub API: {PROJECT_NAME}...")
r = requests.post(url, headers=headers, json=data)

print("\n2. [CRITICAL TEST] Mengambil Username Asli...")
response_data = r.json()
if "owner" in response_data:
    actual_username = response_data["owner"]["login"]
else:
    user_req = requests.get("https://api.github.com/user", headers=headers)
    actual_username = user_req.json().get("login", GITHUB_USERNAME_DI_ENV)

print(f"   -> Username di .env   : {GITHUB_USERNAME_DI_ENV}")
print(f"   -> Username asli (API): {actual_username}")

if actual_username == GITHUB_USERNAME_DI_ENV:
    print("   [!] BAHAYA: Username gagal diperbaiki!")
else:
    print("   [+] SUKSES: Username berhasil dikoreksi otomatis!")

repo_url_auth = f"https://{GITHUB_TOKEN}@github.com/{actual_username}/{PROJECT_NAME}.git"

if os.path.exists(PROJECT_NAME):
    shutil.rmtree(PROJECT_NAME)
os.makedirs(PROJECT_NAME, exist_ok=True)

with open(os.path.join(PROJECT_NAME, "test.txt"), "w") as f:
    f.write("Simulasi ke-2 berhasil membuktikan Git Push Anti-Typo.")

commands = [
    "git init",
    "git config user.email \"vps-agent@ai.local\"",
    "git config user.name \"Immortal Qwen Agent\"",
    "git add .",
    "git commit -m \"Test simulasi anti typo\" --allow-empty",
    "git branch -M main",
    "git remote remove origin",
    f"git remote add origin {repo_url_auth}",
    "git push -u origin main -f"
]

print("\n3. Menjalankan Commands Git Push...")
for cmd in commands:
    safe_cmd = cmd.replace(GITHUB_TOKEN, "***TOKEN***")
    print(f"\n[Execute]: {safe_cmd}")
    
    result = subprocess.run(cmd, shell=True, cwd=PROJECT_NAME, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"  [stdout]: {result.stdout.strip()}")
    if result.stderr.strip() and "error: No such remote" not in result.stderr:
        print(f"  [stderr]: {result.stderr.strip()}")

print("\n=== SIMULASI SUPER SELESAI ===")

