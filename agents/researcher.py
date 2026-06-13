import requests

class ResearcherAgent:
    @staticmethod
    def perform_live_research():
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
