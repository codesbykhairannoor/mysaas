import json
import re
from utils.llm_client import LLMClient
from utils.workspace import Workspace

class EngineerAgent:
    @staticmethod
    def write_initial_code(project_path, idea, design_doc):
        print(f"\n[STEP 4] Menerjemahkan Desain menjadi Multi-File Codebase...")
        prompt = f"""
        You are an elite AI system embodying multiple world-class roles simultaneously:
        1. Paranoid Senior Fullstack Engineer (Next.js 14 App Router, Clean Architecture). You MUST implement robust edge-case handling: Local Video File Uploads (Drag & Drop), strict URL Validation (YouTube/TikTok), Error Boundaries, and Skeleton Loading states.
        2. UI/UX Engineer (Tailwind, Framer Motion, Glassmorphism, Brutalism).
        3. DevOps Engineer (Modular file structure, performance optimization).
        4. Technical SEO & GEO Expert (Super SEO, Multi-language/i18n, structured data).
        5. AI Researcher (Ensuring semantic HTML that is highly friendly to AI bots/crawlers).
        
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
        response_str = LLMClient.query(prompt, require_json=True)
        try:
            match = re.search(r'```(?:json)?\n(.*?)\n```', response_str, re.DOTALL)
            if match:
                response_str = match.group(1).strip()
                
            files_dict = json.loads(response_str)
            Workspace.save_files(project_path, files_dict)
            return files_dict
        except Exception as e:
            print(f"     [!] Gagal memparsing JSON multi-file: {e}")
            return None
