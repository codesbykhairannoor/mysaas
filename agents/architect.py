import json
import re
from utils.llm_client import LLMClient

class ArchitectAgent:
    @staticmethod
    def design_architecture(live_data):
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
            
        return response_text, idea
