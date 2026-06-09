import os
import time
import json
import subprocess
import requests
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

# ==========================================
# KONFIGURASI UNRESTRICTED COGNITIVE AGENT
# ==========================================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
AI_MODEL = os.getenv("AI_MODEL", "qwen-plus")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "username_anda")

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

class UnrestrictedCognitiveAgent:
    def __init__(self, output_dir="./saas_factory"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.design_rules = self._load_design_rules()
        print(f"[*] AGI Agent Started. Factory Mode: UNRESTRICTED.")
        print(f"[*] Brain: {AI_MODEL} | API: {OPENAI_BASE_URL}")
        print(f"[*] Working Directory: {self.output_dir.absolute()}")

    def _load_design_rules(self):
        design_file = Path("design.md")
        if design_file.exists():
            return design_file.read_text(encoding="utf-8")
        return "Use modern, premium web design principles."

    def think_of_idea(self):
        print("\n[STEP 1] Agent sedang memikirkan ide aplikasi mikro yang revolusioner...")
        prompt = """
        You are an elite, unrestricted SaaS founder and SEO God. 
        Think of ONE highly searched, incredibly profitable web tool idea that solves a huge pain point.
        It must be something people search for on Google massively. (e.g. PDF tools, AI generators, Compressors, Converters).
        Output ONLY valid JSON:
        {
            "project_name": "seo-friendly-name-no-spaces",
            "title": "Premium SEO Optimized Title",
            "description": "Short compelling description",
            "features": ["feature 1", "feature 2"],
            "seo_keywords": ["keyword1", "keyword2"]
        }
        """
        try:
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            idea = json.loads(response.choices[0].message.content)
            print(f"[+] Ide Genius Ditemukan: {idea['title']}")
            return idea
        except Exception as e:
            print(f"[!] Error saat memikirkan ide: {e}")
            return None

    def setup_nextjs(self, project_name):
        print(f"\n[STEP 2] Membangun kerangka Next.js untuk {project_name}...")
        project_path = self.output_dir / project_name
        if not project_path.exists():
            # Use non-interactive create-next-app
            cmd = f"npx -y create-next-app@latest {project_name} --typescript --tailwind --eslint --app --src-dir --import-alias \"@/*\" --use-npm"
            subprocess.run(cmd, shell=True, check=True, cwd=str(self.output_dir), stdout=subprocess.DEVNULL)
        return project_path

    def write_initial_code(self, project_path, idea):
        print(f"\n[STEP 3] Menulis draf kode pertama (UI + Logic + Ads + Stripe)...")
        prompt = f"""
        Write the FULL content for `src/app/page.tsx` for a Next.js 14 App Router project.
        Project: {idea['title']} - {idea['description']}
        
        DESIGN SYSTEM TO FOLLOW:
        {self.design_rules}
        
        CRITICAL UNRESTRICTED INSTRUCTIONS:
        1. MUST include placeholder Google AdSense ad slots.
        2. MUST include Stripe Checkout UI components for premium features.
        3. MUST have flawless Next.js metadata generation for SUPER SEO (generateMetadata).
        4. MUST use Tailwind CSS following the DESIGN SYSTEM above (Glassmorphism, Bento, etc.).
        5. Use 'framer-motion' for animations and 'lucide-react' for icons.
        6. Provide fully working UI logic using 'use client' where necessary.
        
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
            
            # Sub-step A: Test the build locally
            print("  -> Menjalankan 'npm run build' untuk quality control...")
            build_success, build_logs = self._test_build(project_path)
            
            # Sub-step B: AI Critic Agent
            critic_prompt = f"""
            You are a harsh Senior Staff Engineer and SEO Expert. Review this Next.js page code.
            Project Idea: {idea['title']}
            Build Status: {'SUCCESS' if build_success else 'FAILED'}
            Build Logs: {build_logs[-1000:] if not build_success else 'No errors.'}
            
            DESIGN SYSTEM:
            {self.design_rules}

            Current Code:
            ```tsx
            {best_code}
            ```
            
            Identify flaws:
            1. Did the build fail? If yes, what is the exact fix?
            2. Is the SEO metadata TRULY optimized?
            3. Are the monetization (Ads/Stripe) prominent enough?
            4. Is the UI actually following the DESIGN SYSTEM?
            
            If it's absolutely perfect and build passes, reply EXACTLY with "PERFECT". 
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

    def _query_ai(self, prompt):
        try:
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            code = response.choices[0].message.content.strip()
            if code.startswith("```"): 
                code = "\n".join(code.split("\n")[1:-1])
            return code
        except Exception as e:
            print(f"[!] API Error: {e}")
            return ""

    def _save_code(self, file_path, code):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

    def publish_to_github(self, project_path, idea):
        if not GITHUB_TOKEN or GITHUB_TOKEN.startswith("ghp_MASUKKAN"):
            print("[!] Skipping GitHub Push: Token not provided.")
            return

        print(f"\n[STEP 5] Mempublikasikan ke GitHub: {idea['project_name']}...")
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "name": idea['project_name'],
            "description": idea['description'],
            "private": False
        }
        
        try:
            requests.post(url, headers=headers, json=data)
            repo_url = f"https://github.com/{GITHUB_USERNAME}/{idea['project_name']}.git"
            
            commands = [
                "git init",
                "git add .",
                "git commit -m \"Unrestricted AI Agent: Super SaaS Auto-Commit\"",
                "git branch -M main",
                f"git remote add origin {repo_url}",
                "git push -u origin main -f"
            ]
            for cmd in commands:
                subprocess.run(cmd, shell=True, cwd=str(project_path), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print(f"[+] SUKSES! Repo Live di: {repo_url}")
        except Exception as e:
            print(f"[!] Gagal publikasi: {e}")

    def run_factory(self, max_projects=3):
        print("\n==================================================================")
        print(f"🚀 UNRESTRICTED SUPER SAAS FACTORY STARTED (LIMIT: {max_projects} WEBS)")
        print("==================================================================")
        
        # Daftar model yang JAUH LEBIH MURAH tapi tetep pinter (Qwen2.5 & Turbo)
        model_pool = ["qwen-turbo", "qwen2.5-72b-instruct", "qwen2.5-coder-32b-instruct", "qwen-plus", "qwen-turbo-latest"]
        project_count = 0
        
        while project_count < max_projects:
            # Rotasi model setiap iterasi biar quota gak gampang habis
            current_model = model_pool[project_count % len(model_pool)]
            print(f"\n[PROJECT {project_count + 1}/{max_projects}] Using Model: {current_model}")
            
            try:
                # Update model global untuk iterasi ini
                global AI_MODEL
                AI_MODEL = current_model
                
                idea = self.think_of_idea()
                if not idea:
                    time.sleep(60); continue
                
                project_path = self.setup_nextjs(idea["project_name"])
                
                print("  -> Menginstall dependencies (lucide-react, framer-motion, stripe)...")
                subprocess.run("npm install lucide-react framer-motion stripe", shell=True, cwd=str(project_path), stdout=subprocess.DEVNULL)
                
                initial_code = self.write_initial_code(project_path, idea)
                self.self_reflect_and_fix(project_path, idea, initial_code)
                self.publish_to_github(project_path, idea)
                
                project_count += 1
                if project_count < max_projects:
                    print(f"\n[!] Project {project_count} Selesai. Istirahat 10 menit sebelum web berikutnya...\n")
                    time.sleep(600) 
                
            except KeyboardInterrupt:
                print("\n[!] Factory dihentikan.")
                break
            except Exception as e:
                print(f"\n[!] Error: {e}. Mencoba model lain dalam 60 detik...")
                time.sleep(60)
        
        print(f"\n==================================================================")
        print(f"✅ TARGET {max_projects} WEB TERCAPAI. Factory Berhenti.")
        print("==================================================================")

if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("[!] ERROR: Masukkan API KEY di .env")
        exit(1)
        
    agent = UnrestrictedCognitiveAgent()
    agent.run_factory()
