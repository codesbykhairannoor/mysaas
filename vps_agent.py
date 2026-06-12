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
# KONFIGURASI "ENTERPRISE ARTISAN AGENT"
# ==========================================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-isi-openai-key-anda-disini")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "ghp_isi-github-token-anda-disini")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "username_anda")

FALLBACK_MODELS = [
    "qwen-turbo",              # Super Cepat, Murah ($0.05 / 1M token)
    "qwen-flash",              # Generasi Flash baru (sangat cepat)
    "qwen-plus",               # Seimbang ($0.40 / 1M token)
]

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

class EnterpriseCognitiveAgent:
    def __init__(self, output_dir="./saas_factory"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        print(f"[*] AGI Agent Started. Mode: ENTERPRISE ARTISAN (Max 2 Web). Working Directory: {self.output_dir.absolute()}")
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
        1. NO PDF TOOLS. Pick a wildly creative, highly profitable enterprise-level web tool idea.
        2. Plan a deep architecture for a Next.js App Router project.
        3. The architecture MUST include strategies for: SUPER SEO, Global GEO Targeting (i18n Multi-language), AI-Friendly structured data, Community Features (forums/comments placeholder), and Enterprise-grade UI/UX.
        
        Write a comprehensive technical `DESIGN.md` document outlining the idea, target audience, and technical implementation plan.
        Make it look extremely professional with markdown headings, tables, and architecture guidelines.
        
        End the document with a JSON block EXACTLY like this (wrapped in ```json):
        ```json
        {{
            "project_name": "seo-friendly-name-no-spaces",
            "title": "Premium SEO Optimized Title",
            "description": "Short compelling description"
        }}
        ```
        """
        response_text = self._query_ai(prompt, require_json=False)
        
        # Ekstrak JSON dari dalam DESIGN.md
        idea = None
        try:
            # Cari semua blok JSON, ambil yang terakhir (karena diinstruksikan di akhir)
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
                # Jika AI lupa pakai markdown fences, cari objek JSON di string
                match = re.search(r'(\{[\s\S]*"project_name"[\s\S]*\})', response_text)
                if match:
                    idea = json.loads(match.group(1).strip())
        except Exception as e:
            print(f"     [!] Error parsing JSON dari DESIGN.md: {e}")
            
        if not idea:
            import random
            random_id = random.randint(1000, 9999)
            idea = {"project_name": f"enterprise-app-{random_id}", "title": f"Enterprise App {random_id}", "description": "Auto-generated"}
            
        return response_text, idea

    def setup_nextjs(self, project_name):
        print(f"\n[STEP 3] Membangun fondasi Enterprise Next.js untuk {project_name}...")
        project_path = self.output_dir / project_name
        if not project_path.exists():
            # Menggunakan versi 14 spesifik agar tidak terblokir oleh pertanyaan interaktif Turbopack di Next.js 15
            cmd = f"npx -y create-next-app@14.2.15 {project_name} --typescript --tailwind --eslint --app --src-dir --import-alias \"@/*\" --use-npm"
            subprocess.run(cmd, shell=True, check=True, cwd=str(self.output_dir), stdout=subprocess.DEVNULL)
        return project_path

    def write_initial_code(self, project_path, idea, design_doc):
        print(f"\n[STEP 4] Menerjemahkan Desain menjadi Multi-File Enterprise Codebase...")
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
        You must generate the complete codebase. Because this is an enterprise app, you MUST NOT put everything in one file. 
        Create at minimum:
        1. `src/app/page.tsx` (Main UI with AI-friendly schema & i18n placeholders)
        2. `src/app/layout.tsx` (Global layout & SEO metadata)
        3. `src/components/...` (Reusable UI/UX components)
        4. `src/lib/...` (Utilities, API mock clients)
        
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
            # Tangani kasus di mana AI tetap memberikan markdown fences ```json
            match = re.search(r'```(?:json)?\n(.*?)\n```', response_str, re.DOTALL)
            if match:
                response_str = match.group(1).strip()
                
            files_dict = json.loads(response_str)
            self._save_files(project_path, files_dict)
            return files_dict
        except Exception as e:
            print(f"     [!] Gagal memparsing JSON multi-file: {e}")
            return None

    def self_reflect_and_fix(self, project_path, idea, current_files, max_iterations=3):
        print(f"\n[STEP 5] EXTREME QUALITY CONTROL: Linting & Build Testing (Multi-File)...")
        best_files = current_files or {}
        
        for i in range(max_iterations):
            print(f"  -> Iterasi Evaluasi ke-{i+1}...")
            print("  -> Menjalankan 'npm run lint' dan 'npm run build'...")
            build_success, build_logs = self._test_build_and_lint(project_path)
            
            # Buat ringkasan file untuk diinfokan ke AI
            file_tree = "\\n".join(best_files.keys())
            
            if not build_success:
                critic_prompt = f"""
                You are a Senior Staff Engineer fixing a BROKEN Enterprise Next.js app.
                The Lint/Build FAILED with these logs:
                {build_logs[-2000:]}
                
                Current files in project:
                {file_tree}
                
                CRITICAL INSTRUCTIONS:
                You MUST fix the errors. DO NOT reply with "PERFECT".
                Identify which files caused the error, and rewrite ONLY the files that need fixing.
                Output a JSON object where keys are the relative file paths and values are the NEW raw code strings.
                Example:
                {{
                    "src/components/BrokenComponent.tsx": "export default function Fixed() {{ ... }}"
                }}
                """
            else:
                critic_prompt = f"""
                You are an Enterprise Software Architect reviewing a Next.js app.
                Lint & Build are SUCCESSFUL.
                Project Idea: {idea.get('title')}
                
                Current files in project:
                {file_tree}
                
                Identify flaws:
                1. Are components modular enough?
                2. Are there any missing imports?
                3. Is the UI highly premium?
                
                If the entire app is absolutely perfect for a Silicon Valley startup, reply EXACTLY with the single word "PERFECT". 
                Otherwise, output a JSON object containing the rewritten/enhanced files (only the files you changed).
                """
            
            response = self._query_ai(critic_prompt, require_json=False)
            clean_resp = response.strip()
            
            is_perfect = clean_resp == "PERFECT" or clean_resp.startswith("PERFECT")
            
            if is_perfect:
                if build_success:
                    print("  [+] Kritis Agen: Seluruh Kode Enterprise SEMPURNA dan lulus Linter/Build! Keluar dari loop.")
                    break
                else:
                    print("  [!] Peringatan: Agen menjawab PERFECT tapi Linter/Build GAGAL! Memaksa iterasi ulang...")
                    continue
            else:
                if not clean_resp:
                    print("  [!] Agen mengembalikan teks kosong, skip save...")
                    continue
                    
                print("  [!] Kritis Agen: Menerapkan perbaikan Multi-File...")
                try:
                    match = re.search(r'```(?:json)?\n(.*?)\n```', clean_resp, re.DOTALL)
                    if match:
                        fixed_files = json.loads(match.group(1).strip())
                    else:
                        fixed_files = json.loads(clean_resp)
                        
                    best_files.update(fixed_files)
                    self._save_files(project_path, fixed_files)
                except Exception as e:
                    print(f"  [!] Gagal memparsing JSON perbaikan (bukan format JSON valid): {e}")
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

    def publish_to_github(self, project_path, idea):
        print(f"\n[STEP 6] Mempublikasikan Karya Enterprise ke GitHub: {idea.get('project_name')}...")
        if not GITHUB_TOKEN or GITHUB_TOKEN == "ghp_isi-github-token-anda-disini":
            print("[!] Token GitHub belum disetel. Melompati upload GitHub.")
            return

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
            
            commands = [
                "git init",
                "git config user.email \"vps-agent@ai.local\"",
                "git config user.name \"Enterprise Artisan Agent\"",
                "git add .",
                "git commit -m \"Initial Enterprise Architecture & Codebase\"",
                "git branch -M main",
                "git remote remove origin", 
                f"git remote add origin {repo_url_auth}",
                "git push -u origin main -f"
            ]
            
            print("     [Mengunggah Repositori...]")
            for cmd in commands:
                subprocess.run(cmd, shell=True, cwd=str(project_path), capture_output=True)
            
            print(f"[+] SUKSES BESAR! Repo Live di: {repo_url_clean}")
        except Exception as e:
            print(f"[!] Gagal publikasi: {e}")

    def run_factory(self):
        print("\n==================================================================")
        print("🚀 THE ENTERPRISE ARTISAN AGENT STARTED (MAX 2 PROJECTS / 6 HOURS)")
        print("==================================================================")
        
        while True:
            for project_number in range(1, 3):
                print(f"\n==================================================================")
                print(f"🛠️ MEMULAI PROYEK ENTERPRISE KE-{project_number} / 2")
                print(f"==================================================================")
                try:
                    live_data = self._perform_live_research()
                    design_doc, idea = self.design_architecture(live_data)
                    
                    project_path = self.setup_nextjs(idea.get("project_name"))
                    
                    # Simpan DESIGN.md
                    self._save_files(project_path, {"DESIGN.md": design_doc})
                    
                    print("  -> Menginstall dependencies (lucide-react, framer-motion)...")
                    subprocess.run("npm install lucide-react framer-motion", shell=True, cwd=str(project_path), stdout=subprocess.DEVNULL)
                    
                    initial_files = self.write_initial_code(project_path, idea, design_doc)
                    if not initial_files:
                        print("[!] Gagal menulis kode.")
                        continue
                    
                    self.self_reflect_and_fix(project_path, idea, initial_files)
                    self.publish_to_github(project_path, idea)
                    
                    print(f"  [🧹] Membersihkan direktori lokal {project_path} untuk menghemat ruang disk VPS...")
                    import shutil
                    shutil.rmtree(project_path, ignore_errors=True)
                    
                    if project_number < 2:
                        print(f"\n[!] Proyek {project_number} Selesai. Istirahat 1 menit sebelum proyek terakhir...\n")
                        time.sleep(60)
                    else:
                        print(f"\n[🎉] SELURUH 2 PROYEK ENTERPRISE TELAH SELESAI! AGEN TIDUR 6 JAM.\n")
                        time.sleep(6 * 60 * 60) # Tidur 6 jam
                    
                except KeyboardInterrupt:
                    print("\n[!] Dihentikan secara manual.")
                    return
                except Exception as e:
                    print(f"\n[!] Error: {e}. Lanjut ke proyek berikutnya jika ada...")
                    time.sleep(10)

if __name__ == "__main__":
    if OPENAI_API_KEY == "sk-isi-openai-key-anda-disini":
        print("[!] ERROR: Masukkan OPENAI_API_KEY valid di file .env")
        exit(1)
        
    agent = EnterpriseCognitiveAgent()
    agent.run_factory()
