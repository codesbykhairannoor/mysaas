import os
import time
import json
import random
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, PermissionDeniedError, RateLimitError, APIError
from duckduckgo_search import DDGS

# ==========================================
# KONFIGURASI "THE IMMORTAL QWEN AGENT"
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

class UnrestrictedCognitiveAgent:
    def __init__(self, output_dir="./saas_factory"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        print(f"[*] AGI Agent Started. Mode: GOD MODE (Web Search + i18n). Working Directory: {self.output_dir.absolute()}")
        print(f"[*] Endpoint: {OPENAI_BASE_URL}")

    def _perform_live_research(self):
        print("\n[STEP 0] Mengakses Internet: Mencari tren keyword micro SaaS tertinggi...")
        queries = [
            "most searched free online utility tools 2026",
            "trending micro saas ideas high volume low competition",
            "most popular ai web tools right now",
            "free online converters highly searched 2026",
            "best single page web utilities for seo"
        ]
        query = random.choice(queries)
        results_text = ""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=4))
                for r in results:
                    results_text += f"- {r.get('title')}: {r.get('body')}\n"
            print("     [+] Berhasil mendapatkan data intelijen dari Google/DDG!")
            return results_text
        except Exception as e:
            print(f"     [!] Pencarian web gagal, menggunakan database internal AI: {e}")
            return "No live data. Use your brilliant internal knowledge."

    def think_of_idea(self):
        live_data = self._perform_live_research()
        
        print(f"\n[STEP 1] Agent merumuskan ide brilian berdasarkan data internet...")
        prompt = f"""
        You are an elite, unrestricted SaaS founder and an absolute SEO God. 
        I have provided you with live web search data about currently trending utility tools:
        
        {live_data}
        
        CRITICAL DOCTRINE:
        1. DO NOT MAKE PDF TOOLS! We already have too many PDF tools. BE CREATIVE.
        2. Pick ONE incredibly profitable, high search-volume utility tool idea.
        3. It must be highly requested globally, easy to build as a single-page Next.js app, and solve a MASSIVE pain point.
        4. Examples of allowed categories (Pick anything fresh): AI Text Generators, Video Summarizers, Image Upscalers, Regex Testers, SEO Analyzers, CSS Generators, Language Translators, etc.
        
        Output ONLY valid JSON:
        {{
            "project_name": "seo-friendly-name-no-spaces",
            "title": "Premium SEO Optimized Title",
            "description": "Short compelling description",
            "features": ["feature 1", "feature 2"],
            "seo_keywords": ["keyword1", "keyword2"]
        }}
        """
        response_text = self._query_ai(prompt, require_json=True)
        if not response_text:
            return None
        
        try:
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            idea = json.loads(response_text.strip())
            print(f"[+] Ide Genius Ditemukan: {idea.get('title', 'Unknown')}")
            return idea
        except Exception as e:
            print(f"[!] Error decoding JSON ide: {e}\nRaw Response: {response_text}")
            return None

    def setup_nextjs(self, project_name):
        print(f"\n[STEP 2] Membangun kerangka Next.js untuk {project_name}...")
        project_path = self.output_dir / project_name
        if not project_path.exists():
            cmd = f"npx -y create-next-app@latest {project_name} --typescript --tailwind --eslint --app --src-dir --import-alias \"@/*\" --use-npm"
            subprocess.run(cmd, shell=True, check=True, cwd=str(self.output_dir), stdout=subprocess.DEVNULL)
        return project_path

    def write_initial_code(self, project_path, idea):
        print(f"\n[STEP 3] Menulis draf kode (UI + Logic + Ads + Stripe + i18n)...")
        prompt = f"""
        Write the FULL content for `src/app/page.tsx` for a Next.js 14 App Router project.
        Project: {idea.get('title')} - {idea.get('description')}
        
        CRITICAL UNRESTRICTED INSTRUCTIONS:
        1. MUST include placeholder Google AdSense ad slots (e.g. <div className="adsense-slot">).
        2. MUST include Stripe / PayPal Checkout UI components for premium features.
        3. MUST have flawless Next.js metadata generation for SUPER SEO.
        4. MUST use Tailwind CSS with an ultra-premium, modern, glassmorphism UI.
        5. MUST INCLUDE Multi-Language (i18n) support built-in (e.g., UI elements that can switch languages to dominate Global GEO SEO).
        6. Provide fully working UI logic using 'use client' where necessary, or structure it properly if server-rendered.
        
        OUTPUT ONLY THE RAW TYPESCRIPT CODE. No markdown fences.
        """
        code = self._query_ai(prompt)
        self._save_code(project_path / "src" / "app" / "page.tsx", code)
        return code

    def self_reflect_and_fix(self, project_path, idea, current_code, max_iterations=3):
        print(f"\n[STEP 4] MIKIR PHASE: Self-Reflection & Testing Loop...")
        best_code = current_code
        
        for i in range(max_iterations):
            print(f"  -> Iterasi Evaluasi ke-{i+1}...")
            print("  -> Menjalankan 'npm run build' untuk quality control...")
            build_success, build_logs = self._test_build(project_path)
            
            critic_prompt = f"""
            You are a harsh Senior Staff Engineer and SEO Expert. Review this Next.js page code.
            Project Idea: {idea.get('title')}
            Build Status: {'SUCCESS' if build_success else 'FAILED'}
            Build Logs: {build_logs[-1000:] if not build_success else 'No errors.'}
            
            Current Code:
            ```tsx
            {best_code}
            ```
            
            Identify flaws:
            1. Did the build fail? If yes, what is the exact fix?
            2. Is the SEO metadata TRULY optimized?
            3. Are the monetization (Ads/Stripe) prominent enough?
            4. Is the UI actually premium?
            5. Is Multi-Language (i18n) properly implemented?
            
            If it's absolutely perfect and build passes, reply EXACTLY with the single word "PERFECT". 
            Otherwise, rewrite the FULL, FIXED, AND ENHANCED code. ONLY output raw code, no explanations.
            """
            
            response = self._query_ai(critic_prompt)
            
            if response.strip() == "PERFECT" and build_success:
                print("  [+] Kritis Agen: Kode sudah SEMPURNA dan lulus Build! Keluar dari loop.")
                break
            else:
                print("  [!] Kritis Agen: Menemukan kekurangan. Menerapkan kode yang lebih baik...")
                best_code = response
                self._save_code(project_path / "src" / "app" / "page.tsx", best_code)
                
        return best_code

    def _test_build(self, project_path):
        try:
            result = subprocess.run("npm run build", shell=True, cwd=str(project_path), capture_output=True, text=True)
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)

    def _query_ai(self, prompt, require_json=False):
        for model_name in FALLBACK_MODELS:
            print(f"     [>] Mencoba memanggil API dengan model: {model_name}...")
            try:
                response_format = {"type": "json_object"} if require_json else None
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    response_format=response_format
                )
                
                code = response.choices[0].message.content.strip()
                if code.startswith("```tsx"): code = code[6:]
                elif code.startswith("```typescript"): code = code[14:]
                elif code.startswith("```"): code = code[3:]
                if code.endswith("```"): code = code[:-3]
                
                return code.strip()
                
            except PermissionDeniedError:
                print(f"     [X] Error 403: Akses ditolak untuk model '{model_name}'. Melompat ke model cadangan...")
                continue
            except RateLimitError:
                print(f"     [X] Error 429: Rate Limit tercapai untuk model '{model_name}'. Melompat ke model cadangan...")
                time.sleep(2)
                continue
            except APIError as e:
                print(f"     [X] API Error pada model '{model_name}': {e}. Melompat ke model cadangan...")
                continue
            except Exception as e:
                print(f"     [X] Error tak terduga pada model '{model_name}': {e}. Melompat ke model cadangan...")
                continue
                
        print("[!!!] FATAL ERROR: Semua 5 model cadangan telah dicoba dan semuanya gagal! Menyerah untuk siklus ini.")
        return ""

    def _save_code(self, file_path, code):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

    def publish_to_github(self, project_path, idea):
        print(f"\n[STEP 5] Mempublikasikan ke GitHub: {idea.get('project_name')}...")
        if not GITHUB_TOKEN or GITHUB_TOKEN == "ghp_isi-github-token-anda-disini":
            print("[!] Token GitHub belum disetel. Melompati proses upload GitHub.")
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
            requests.post(url, headers=headers, json=data) # Mengabaikan respon 422 (repo exists)
            repo_url_auth = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{idea.get('project_name')}.git"
            repo_url_clean = f"https://github.com/{GITHUB_USERNAME}/{idea.get('project_name')}.git"
            
            commands = [
                "git init",
                "git config user.email \"vps-agent@ai.local\"",
                "git config user.name \"Immortal Qwen Agent\"",
                "git add .",
                "git commit -m \"Unrestricted AI Agent Auto-Commit: SEO & Premium UI\"",
                "git branch -M main",
                "git remote remove origin", 
                f"git remote add origin {repo_url_auth}",
                "git push -u origin main -f"
            ]
            
            print("     [Mengunggah ke GitHub...]")
            for cmd in commands:
                safe_cmd = cmd.replace(GITHUB_TOKEN, "***TOKEN***")
                result = subprocess.run(cmd, shell=True, cwd=str(project_path), capture_output=True, text=True)
                
                if result.stdout.strip(): print(f"       [Git] {result.stdout.strip()}")
                if result.stderr.strip() and "error: No such remote" not in result.stderr: 
                    print(f"       [Git Log] {result.stderr.strip()}")
            
            print(f"[+] SUKSES BESAR! Repo Live di: {repo_url_clean}")
        except Exception as e:
            print(f"[!] Gagal publikasi: {e}")

    def run_factory(self):
        print("\n==================================================================")
        print("🚀 THE IMMORTAL QWEN FACTORY STARTED (PRESS CTRL+C TO STOP)")
        print("==================================================================")
        
        while True:
            try:
                idea = self.think_of_idea()
                if not idea:
                    time.sleep(10); continue
                
                project_path = self.setup_nextjs(idea.get("project_name"))
                
                print("  -> Menginstall dependencies pendukung (lucide-react, framer-motion, stripe, duckduckgo-search)...")
                subprocess.run("npm install lucide-react framer-motion stripe", shell=True, cwd=str(project_path), stdout=subprocess.DEVNULL)
                
                initial_code = self.write_initial_code(project_path, idea)
                if not initial_code:
                    print("[!] Gagal menulis kode. Mengulang siklus...")
                    continue
                
                self.self_reflect_and_fix(project_path, idea, initial_code)
                self.publish_to_github(project_path, idea)
                
                print(f"\n[!] Mission Accomplished. Istirahat 2 menit sebelum membuat web berikutnya...\n")
                time.sleep(120) 
                
            except KeyboardInterrupt:
                print("\n[!] Factory dihentikan secara manual.")
                break
            except Exception as e:
                print(f"\n[!] Global Factory Error: {e}. Melakukan restart loop dalam 30 detik...")
                time.sleep(30)


if __name__ == "__main__":
    if OPENAI_API_KEY == "sk-isi-openai-key-anda-disini":
        print("[!] ERROR: Anda harus memasukkan OPENAI_API_KEY yang valid di file .env sebelum menjalankan bot ini.")
        exit(1)
        
    agent = UnrestrictedCognitiveAgent()
    agent.run_factory()
