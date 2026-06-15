import json
import re
from utils.llm_client import LLMClient

class ArchitectAgent:
    @staticmethod
    def design_architecture(live_data):
        print(f"\n[STEP 2] Agent bertindak sebagai Chief Architect: Merancang DESIGN.md...")
        prompt = f"""
        You are an elite Silicon Valley Chief Software Architect.
        Analyze this recent live market data (if any):
        {live_data}
        
        CRITICAL DOCTRINE:
        1. USER DIRECTIVE: You MUST build a massive, all-encompassing "Video Summarizer SaaS". Do NOT limit it to just YouTube/TikTok links! You MUST include features for: Local Video Uploads, robust URL Validation, and Edge Case handling.
        2. Act as a Paranoid Senior Architect. Think: "What if the user uploads a local file?", "How do we validate links?", "How do we handle long processing times?".
        3. Plan a deep architecture for a Next.js App Router project for this SaaS.
        4. The architecture MUST include strategies for: SUPER SEO, Global GEO Targeting (i18n Multi-language), AI-Friendly structured data, and Enterprise-grade UI/UX.
        
        Write a comprehensive technical `DESIGN.md` document outlining the Video Summarizer idea, target audience, and technical implementation plan.
        Make it look extremely professional with markdown headings, tables, and architecture guidelines.
        
        End the document with a JSON block EXACTLY like this (wrapped in ```json):
        ```json
        {{
            "project_name": "video-summarizer-saas",
            "title": "Video Summarizer AI",
            "description": "Short compelling description"
        }}
        ```
        """
        response_text = LLMClient.query(prompt, require_json=False)
        
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
            return ArchitectAgent.design_architecture(live_data)
            
        idea['project_name'] = idea['project_name'].lower().replace(" ", "-")
            
        return response_text, idea
