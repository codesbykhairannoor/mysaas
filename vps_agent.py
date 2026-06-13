import os
import time
import json
import random
import subprocess
import requests
import re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, PermissionDeniedError, RateLimitError, APIError

# ==========================================
# KONFIGURASI "DEDICATED SAAS ENGINEER"
# ==========================================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-isi-openai-key-anda-disini")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "ghp_isi-github-token-anda-disini")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "username_anda")

FALLBACK_MODELS = [
    "qwen-turbo",              
    "qwen-flash",              
    "qwen-plus",               
]

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

class EnterpriseCognitiveAgent:
    def __init__(self, output_dir="./saas_factory"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        print(f"[*] AGI Agent Started. Mode: DEDICATED SAAS ENGINEER (1 Repo, Deep Iteration). Working Directory: {self.output_dir.absolute()}")
        print(f"[*] Endpoint: {OPENAI_BASE_URL}")

    def _perform_live_research(self):
        print("\n[STEP 1] Mengakses Internet: Riset Pasar & Tren Global (HackerNews)...")
        results_text = ""
        try:
            top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            top_stories = requests.get(top_stories_url, timeout=10).json()[:8]
            
            for story_id in top_stories:
                story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=10).json()
                if story and 'title' in story:
                    results_text += f"- Tren saat ini: {story.get('title')}\n"
                    
            print("     [+] Berhasil memanen intelijen pasar!")
            return results_text
        except Exception as e:
            print(f"     [!] Koneksi internet gagal: {e}")
            return "No live data. Use your brilliant internal knowledge."

    def design_architecture(self, live_data):
        print(f"\n[STEP 2] Agent bertindak sebagai Chief Architect: Merancang DESIGN.md...")
        prompt = f"""
        You are an elite Silicon Valley Chief Software Architect.
        Analyze this recent live market data:
        {live_data}
        
        CRITICAL DOCTRINE:
        1. NO PDF TOOLS. Pick a wildly creative, highly profitable HIGH-TRAFFIC SaaS idea.
        2. Plan a deep architecture for a Next.js App Router project.
        3. The architecture MUST include strategies for: SUPER SEO, Global GEO Targeting (i18n Multi-language), AI-Friendly structured data, Community Features, and Enterprise-grade UI/UX.
        
        Write a comprehensive technical `DESIGN.md` document outlining the idea, target audience, and technical implementation plan.
        Make it look extremely professional with markdown headings, tables, and architecture guidelines.
        
        End the document with a JSON block EXACTLY like this (wrapped in ```json):
        ```json
        {{
            "project_name": "high-traffic-saas-name-no-spaces",
            "title": "Premium SaaS Name",
            "description": "Short compelling description"
        }}
        ```
        """
        response_text = self._query_ai(prompt, require_json=False)
        
        # Ekstrak JSON dari dalam DESIGN.md
        idea = None
        try:
            matches = re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            for m in reversed(matches):
                try:
                    parsed = json.loads(m.strip())
                    if "project_name" in parsed:
                        idea = parsed
                        break
                except:
                    pass
                    
            if not idea:
                match = re.search(r'(\{[\s\S]*"project_name"[\s\S]*\})', response_text)
                if match:
                    idea = json.loads(match.group(1).strip())
        except Exception as e:
            print(f"     [!] Error parsing JSON dari DESIGN.md: {e}")
            
        if not idea:
            print("     [!] Gagal memparsing JSON dari AI. Memaksa AI mengulang agar tidak memakai nama sembarangan...")
            # Recursive call to force a proper name, preventing "enterprise-app" fallback
            return self.design_architecture(live_data)
            
        return response_text, idea

    def setup_nextjs(self, project_name):
        print(f"\n[STEP 3] Membangun fondasi Enterprise Next.js untuk {project_name}...")
        project_path = self.output_dir / project_name
        if not project_path.exists():
            cmd = f"npx -y create-next-app@14.2.15 {project_name} --typescript --tailwind --eslint --app --src-dir --import-alias \"@/*\" --use-npm"
            subprocess.run(cmd, shell=True, check=True, cwd=str(self.output_dir), stdout=subprocess.DEVNULL)
        return project_path

    def write_initial_code(self, project_path, idea, design_doc):
        print(f"\n[STEP 4] Menerjemahkan Desain menjadi Multi-File Codebase...")
        prompt = f"""
        You are an elite AI system embodying multiple world-class roles simultaneously:
        1. Fullstack Engineer (Next.js 14 App Router, Clean Architecture)
        2. UI/UX Engineer (Tailwind, Framer Motion, Glassmorphism, Brutalism)
        3. DevOps Engineer (Modular file structure, performance optimization)
        4. Technical SEO & GEO Expert (Super SEO, Multi-language/i18n, structured data)
        5. AI Researcher (Ensuring semantic HTML that is highly friendly to AI bots/crawlers)
        
        Project: {idea.get('title')}
        
        Read this Architecture Document:
        {design_doc[:1000]}
        
        CRITICAL ENTERPRISE INSTRUCTIONS:
        You must generate the complete codebase. Because this is a high-traffic SaaS, you MUST NOT put everything in one file. 
        Create at minimum:
        1. `src/app/page.tsx` (Main UI with AI-friendly schema & i18n placeholders)
        2. `src/app/layout.tsx` (Global layout & SEO metadata)
        3. `src/components/...` (Reusable UI/UX components)
        4. `src/lib/...` (Utilities, API mock clients)
        
        DESIGN AESTHETICS (CRITICAL):
        You MUST use stunning, premium designs. Use curated vibrant colors, glassmorphism (backdrop-blur), deep shadows, modern typography, and smooth framer-motion micro-animations. DO NOT generate generic, plain white, simple designs. It must look like an award-winning Silicon Valley SaaS.
        
        OUTPUT FORMAT:
        You MUST output a valid JSON object. Do not include markdown fences around the JSON, just raw JSON.
        The keys must be the relative file paths. The values must be the exact raw code strings.
        Example:
        {{
            "src/app/page.tsx": "import Hero from '@/components/Hero';\\nexport default function Page() {{ return <Hero /> }}",
            "src/components/Hero.tsx": "export default function Hero() {{ return <div>Hero</div> }}"
        }}
        """
        response_str = self._query_ai(prompt, require_json=True)
        try:
            match = re.search(r'```(?:json)?\n(.*?)\n```', response_str, re.DOTALL)
            if match:
                response_str = match.group(1).strip()
                
            files_dict = json.loads(response_str)
            self._save_files(project_path, files_dict)
            return files_dict
        except Exception as e:
            print(f"     [!] Gagal memparsing JSON multi-file: {e}")
            return None

    def continuous_development_loop(self, project_path, idea, current_files, max_iterations=15):
        print(f"\n[STEP 5] DEDICATED ENGINEERING: Continuous Development Loop (Max {max_iterations} Iterations)...")
        best_files = current_files or {}
        
        for i in range(max_iterations):
            print(f"\n  ========================================")
            print(f"  -> Iterasi Pengembangan ke-{i+1} / {max_iterations}...")
            print("  -> Menjalankan 'npm run lint' dan 'npm run build'...")
            build_success, build_logs = self._test_build_and_lint(project_path)
            
            file_tree = "\\n".join(best_files.keys())
            
            if not build_success:
                print("  [X] Build/Lint GAGAL. AI akan fokus memperbaiki error.")
                critic_prompt = f"""
                You are a Senior Staff Engineer fixing a BROKEN High-Traffic Next.js SaaS.
                The Lint/Build FAILED with these logs:
                {build_logs[-2000:]}
                
                Current files in project:
                {file_tree}
                
                CRITICAL INSTRUCTIONS:
                You MUST fix the errors. DO NOT reply with "PERFECT".
                Identify which files caused the error, and rewrite ONLY the files that need fixing.
                Output a JSON object where keys are the relative file paths and values are the NEW raw code strings.
                """
                commit_msg = f"fix: resolve build and lint errors (Iteration {i+1})"
            else:
                print("  [+] Build/Lint SUKSES. AI akan fokus menambahkan fitur & mempercantik UI.")
                critic_prompt = f"""
                You are a World-Class Product Manager and UI/UX Designer.
                The Next.js app builds perfectly.
                Project Idea: {idea.get('title')}
                
                Current files in project:
                {file_tree}
                
                CRITICAL MISSION:
                Do NOT stop. We need to turn this into a massively profitable High-Traffic SaaS.
                Analyze the current files and invent a NEW brilliant feature, OR significantly improve the UI aesthetics (add Glassmorphism, animations, gradients).
                Output a JSON object containing the NEW or REWRITTEN files.
                If you absolutely cannot improve it further, output EXACTLY "PERFECT".
                """
                commit_msg = f"feat: continuous UI/UX and feature enhancement (Iteration {i+1})"
            
            response = self._query_ai(critic_prompt, require_json=False)
            clean_resp = response.strip()
            
            is_perfect = clean_resp == "PERFECT" or clean_resp.startswith("PERFECT")
            
            if is_perfect:
                print("  [+] Kritis Agen: Aplikasi sudah mencapai tingkat dewa. Keluar dari loop pengembangan.")
                break
            else:
                if not clean_resp:
                    print("  [!] Agen mengembalikan teks kosong, skip save...")
                    continue
                    
                print("  [!] Mengaplikasikan iterasi perbaikan / fitur baru...")
                try:
                    match = re.search(r'```(?:json)?\n(.*?)\n```', clean_resp, re.DOTALL)
                    if match:
                        fixed_files = json.loads(match.group(1).strip())
                    else:
                        fixed_files = json.loads(clean_resp)
                        
                    best_files.update(fixed_files)
                    self._save_files(project_path, fixed_files)
                    self._git_commit(project_path, commit_msg)
                    
                    # Push incremental ke GitHub
                    print("  [Mengunggah komit terbaru ke GitHub...]")
                    subprocess.run("git push -u origin main -f", shell=True, cwd=str(project_path), capture_output=True)
                except Exception as e:
                    print(f"  [!] Gagal memparsing JSON perbaikan: {e}")
                    continue
                
        return best_files

    def _test_build_and_lint(self, project_path):
        try:
            lint = subprocess.run("npm run lint", shell=True, cwd=str(project_path), capture_output=True, text=True)
            build = subprocess.run("npm run build", shell=True, cwd=str(project_path), capture_output=True, text=True)
            
            success = (lint.returncode == 0) and (build.returncode == 0)
            logs = f"LINT LOGS:\n{lint.stdout}\n{lint.stderr}\n\nBUILD LOGS:\n{build.stdout}\n{build.stderr}"
            return success, logs
        except Exception as e:
            return False, str(e)

    def _query_ai(self, prompt, require_json=False):
        for model_name in FALLBACK_MODELS:
            print(f"     [>] Memanggil AI ({model_name})...")
            try:
                response_format = {"type": "json_object"} if require_json else None
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    response_format=response_format
                )
                
                content = response.choices[0].message.content.strip()
                
                if not require_json and content != "PERFECT":
                    match = re.search(r'```(?:tsx|typescript|ts|javascript|js)?\n(.*?)\n```', content, re.DOTALL)
                    if match:
                        content = match.group(1).strip()
                    elif content.startswith("```"):
                        content = content.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
                
                return content.strip()
                
            except PermissionDeniedError:
                print(f"     [X] Error 403 ({model_name}). Melompat ke cadangan...")
                continue
            except RateLimitError:
                print(f"     [X] Error 429 ({model_name}). Melompat ke cadangan...")
                time.sleep(2)
                continue
            except Exception as e:
                print(f"     [X] Error tak terduga ({model_name}): {e}")
                continue
                
        print("[!!!] FATAL ERROR: Semua model gagal!")
        return ""

    def _save_files(self, project_path, files_dict):
        for rel_path, code in files_dict.items():
            rel_path = rel_path.lstrip("/")
            file_path = project_path / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

    def _git_commit(self, project_path, message):
        commands = [
            "git add .",
            f'git commit -m "{message}"'
        ]
        for cmd in commands:
            subprocess.run(cmd, shell=True, cwd=str(project_path), capture_output=True)

    def _create_github_repo(self, idea):
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

    def run_factory(self):
        print("\n==================================================================")
        print("🚀 THE DEDICATED SAAS ENGINEER STARTED (1 Repo, Deep Iteration)")
        print("==================================================================")
        
        try:
            live_data = self._perform_live_research()
            design_doc, idea = self.design_architecture(live_data)
            
            # 1. Setup Next.js
            project_path = self.setup_nextjs(idea.get("project_name"))
            
            # Inisialisasi Git & Commits awal
            subprocess.run("git init", shell=True, cwd=str(project_path), capture_output=True)
            subprocess.run("git config user.email \"vps-agent@ai.local\"", shell=True, cwd=str(project_path), capture_output=True)
            subprocess.run("git config user.name \"Dedicated SaaS Engineer\"", shell=True, cwd=str(project_path), capture_output=True)
            subprocess.run("git branch -M main", shell=True, cwd=str(project_path), capture_output=True)
            self._git_commit(project_path, "chore: setup Next.js 14 high-traffic boilerplate")
            
            # Buat Repositori GitHub
            repo_urls = self._create_github_repo(idea)
            if repo_urls:
                repo_url_auth, repo_url_clean = repo_urls
                subprocess.run("git remote remove origin", shell=True, cwd=str(project_path), capture_output=True)
                subprocess.run(f"git remote add origin {repo_url_auth}", shell=True, cwd=str(project_path), capture_output=True)
            
            # 2. DESIGN.md
            self._save_files(project_path, {"DESIGN.md": design_doc})
            self._git_commit(project_path, "docs: initialize enterprise architecture DESIGN.md")
            
            # 3. Dependencies
            print("  -> Menginstall dependencies (lucide-react, framer-motion)...")
            subprocess.run("npm install lucide-react framer-motion", shell=True, cwd=str(project_path), stdout=subprocess.DEVNULL)
            self._git_commit(project_path, "build: install lucide-react and framer-motion")
            
            # 4. Initial Code
            initial_files = self.write_initial_code(project_path, idea, design_doc)
            if not initial_files:
                print("[!] Gagal menulis kode awal. Berhenti.")
                return
            self._git_commit(project_path, "feat: implement initial multi-file UI components and pages")
            
            # Push awal
            if repo_urls:
                print("  [Mengunggah pondasi ke GitHub...]")
                subprocess.run("git push -u origin main -f", shell=True, cwd=str(project_path), capture_output=True)
            
            # 5. Dedicated Continuous Development Loop
            self.continuous_development_loop(project_path, idea, initial_files)
            
            print(f"  [🧹] Membersihkan direktori lokal {project_path} untuk menghemat ruang disk VPS...")
            import shutil
            shutil.rmtree(project_path, ignore_errors=True)
            
        except KeyboardInterrupt:
            print("\n[!] Dihentikan secara manual.")
        except Exception as e:
            print(f"\n[!] Fatal Error: {e}.")

        # Matikan PM2 secara permanen setelah 1 project didedikasikan secara penuh
        print(f"\n[🎉] PENGEMBANGAN SAAS SELESAI SECARA MENYELURUH! MEMBUNUH PROSES PM2 AGAR TIDAK LOOPING.\n")
        subprocess.run("pm2 stop qwen-factory", shell=True)


if __name__ == "__main__":
    if OPENAI_API_KEY == "sk-isi-openai-key-anda-disini":
        print("[!] ERROR: Masukkan OPENAI_API_KEY valid di file .env")
        exit(1)
        
    agent = EnterpriseCognitiveAgent()
    agent.run_factory()
