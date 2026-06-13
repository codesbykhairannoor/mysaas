import os
import subprocess
from utils.workspace import Workspace
from utils.git_manager import GitManager
from agents.researcher import ResearcherAgent
from agents.architect import ArchitectAgent
from agents.engineer import EngineerAgent
from agents.qa_engineer import QAEngineerAgent

class Orchestrator:
    @staticmethod
    def run():
        print("\n==================================================================")
        print("🚀 THE DEDICATED SAAS ENGINEER STARTED (Multi-Agent Architecture)")
        print("==================================================================")
        
        try:
            live_data = ResearcherAgent.perform_live_research()
            design_doc, idea = ArchitectAgent.design_architecture(live_data)
            
            # 1. Setup Next.js
            workspace = Workspace()
            project_path = workspace.setup_nextjs(idea.get("project_name"))
            
            # Buat Repositori GitHub & Inisialisasi Git
            repo_urls = GitManager.create_repo(idea)
            GitManager.initialize_repo(project_path, repo_urls)
            GitManager.commit(project_path, "chore: setup Next.js 14 high-traffic boilerplate")
            
            # 2. DESIGN.md
            Workspace.save_files(project_path, {"DESIGN.md": design_doc})
            GitManager.commit(project_path, "docs: initialize enterprise architecture DESIGN.md")
            
            # 3. Dependencies
            Workspace.install_dependencies(project_path, "lucide-react framer-motion")
            GitManager.commit(project_path, "build: install lucide-react and framer-motion")
            
            # 4. Initial Code
            initial_files = EngineerAgent.write_initial_code(project_path, idea, design_doc)
            if not initial_files:
                print("[!] Gagal menulis kode awal. Berhenti.")
                return
            GitManager.commit(project_path, "feat: implement initial multi-file UI components and pages")
            
            # Push awal
            if repo_urls:
                GitManager.push(project_path)
            
            # 5. Dedicated Continuous Development Loop
            QAEngineerAgent.continuous_development_loop(project_path, idea, initial_files)
            
            Workspace.clean_workspace(project_path)
            
        except KeyboardInterrupt:
            print("\n[!] Dihentikan secara manual.")
        except Exception as e:
            print(f"\n[!] Fatal Error: {e}.")

        # Matikan PM2 secara permanen setelah 1 project didedikasikan secara penuh
        print(f"\n[🎉] PENGEMBANGAN SAAS SELESAI SECARA MENYELURUH! MEMBUNUH PROSES PM2 AGAR TIDAK LOOPING.\n")
        subprocess.run("pm2 stop qwen-factory", shell=True)

if __name__ == "__main__":
    if os.getenv("OPENAI_API_KEY") == "sk-isi-openai-key-anda-disini" or not os.getenv("OPENAI_API_KEY"):
        print("[!] ERROR: Masukkan OPENAI_API_KEY valid di file .env")
        exit(1)
        
    Orchestrator.run()
