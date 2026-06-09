import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import time

def fetch_desc(startup):
    url = startup['url']
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            # The description on trustmrr usually is in a meta description or a specific paragraph
            # Let's try meta description first
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                desc = meta_desc['content']
                # Sometimes meta desc is generic "The database of verified startup revenues..."
                if "database of verified startup revenues" not in desc.lower():
                    startup['description'] = desc.strip()
                    return startup
            
            # If generic or no meta, look for h2 or p tags that might be description
            # Usually there is an h1 with the name, and a p tag next to it
            h1 = soup.find('h1')
            if h1:
                sibling_p = h1.find_next_sibling('p')
                if sibling_p:
                    startup['description'] = sibling_p.text.strip()
                    return startup
            
            startup['description'] = "No description found."
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        startup['description'] = "Failed to fetch description."
    return startup

def main():
    with open("startups.json", "r", encoding="utf-8") as f:
        startups = json.load(f)
        
    print(f"Fetching descriptions for {len(startups)} startups...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        startups = list(executor.map(fetch_desc, startups))
        
    with open("startups_detailed.json", "w", encoding="utf-8") as f:
        json.dump(startups, f, indent=2)
        
    for s in startups[:5]:
        print(f"{s['name']}: {s.get('description', '')}")

if __name__ == "__main__":
    main()
