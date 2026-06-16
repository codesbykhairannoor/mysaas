import json
import re
import subprocess
import time
from utils.llm_client import LLMClient
from utils.workspace import Workspace
from utils.git_manager import GitManager

class QAEngineerAgent:
    @staticmethod
    def _test_build_and_lint(project_path):
        try:
            lint = subprocess.run("npm run lint", shell=True, cwd=str(project_path), capture_output=True, text=True)
            build = subprocess.run("npm run build", shell=True, cwd=str(project_path), capture_output=True, text=True)
            
            success = (lint.returncode == 0) and (build.returncode == 0)
            logs = f"LINT LOGS:\n{lint.stdout}\n{lint.stderr}\n\nBUILD LOGS:\n{build.stdout}\n{build.stderr}"
            return success, logs
        except Exception as e:
            return False, str(e)

    @staticmethod
    def continuous_development_loop(project_path, idea, current_files, max_iterations=100):
        print(f"\n[STEP 5] DEDICATED ENGINEERING: Continuous Development Loop (Max {max_iterations} Iterations / 12 Hours)...")
        best_files = current_files or {}
        start_time = time.time()
        max_duration = 12 * 3600  # 12 Jam dalam detik
        
        for i in range(max_iterations):
            if time.time() - start_time > max_duration:
                print("\n  [!] Kritis Agen: Batas waktu maksimal 12 Jam telah tercapai! Menghentikan pengembangan secara paksa.")
                break
                
            print(f"\n  ========================================")
            print(f"  -> Iterasi Pengembangan ke-{i+1} / {max_iterations}...")
            print("  -> Menjalankan 'npm run lint' dan 'npm run build'...")
            build_success, build_logs = QAEngineerAgent._test_build_and_lint(project_path)
            
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
            
            response = LLMClient.query(critic_prompt, require_json=False)
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
                    Workspace.save_files(project_path, fixed_files)
                    GitManager.commit(project_path, commit_msg)
                    GitManager.push(project_path)
                except Exception as e:
                    print(f"  [!] Gagal memparsing JSON perbaikan: {e}")
                    continue
                
        return best_files
