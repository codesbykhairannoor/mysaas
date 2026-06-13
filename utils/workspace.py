import subprocess
import shutil
from pathlib import Path

class Workspace:
    def __init__(self, output_dir="./saas_factory"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def setup_nextjs(self, project_name):
        print(f"\n[STEP 3] Membangun fondasi Enterprise Next.js untuk {project_name}...")
        project_path = self.output_dir / project_name
        if not project_path.exists():
            cmd = f"npx -y create-next-app@14.2.15 {project_name} --typescript --tailwind --eslint --app --src-dir --import-alias \"@/*\" --use-npm"
            subprocess.run(cmd, shell=True, check=True, cwd=str(self.output_dir), stdout=subprocess.DEVNULL)
        return project_path

    @staticmethod
    def save_files(project_path, files_dict):
        for rel_path, code in files_dict.items():
            rel_path = rel_path.lstrip("/")
            file_path = project_path / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

    @staticmethod
    def clean_workspace(project_path):
        print(f"  [🧹] Membersihkan direktori lokal {project_path} untuk menghemat ruang disk VPS...")
        shutil.rmtree(project_path, ignore_errors=True)

    @staticmethod
    def install_dependencies(project_path, deps):
        print(f"  -> Menginstall dependencies ({deps})...")
        subprocess.run(f"npm install {deps}", shell=True, cwd=str(project_path), stdout=subprocess.DEVNULL)
