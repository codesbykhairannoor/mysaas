import json
from bs4 import BeautifulSoup

def extract_startups():
    with open(r"C:\Users\Axioo\.gemini\antigravity-ide\brain\72e4a70f-81f8-45fa-b276-58990a5a4e73\.system_generated\steps\5\content.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    startups = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/startup/') and href != '/startup/':
            name_tag = a.find('h3')
            if not name_tag:
                continue
            name = name_tag.text.strip()
            
            # The structure has Revenue, Price, Multiple usually in p tags
            metrics = a.find_all('p', class_='font-mono')
            if len(metrics) == 3:
                revenue_str = metrics[0].text.strip()
                price_str = metrics[1].text.strip()
                multiple_str = metrics[2].text.strip()
                
                # Extract category
                category = ""
                cat_tag = a.find('p', class_='truncate')
                if cat_tag:
                    category = cat_tag.text.strip()
                
                # convert to numbers
                def parse_money(m):
                    m = m.replace('$', '').replace(',', '').strip()
                    if m.lower().endswith('k'):
                        return float(m[:-1]) * 1000
                    if m.lower().endswith('m'):
                        return float(m[:-1]) * 1000000
                    try:
                        return float(m)
                    except:
                        return 0
                
                revenue = parse_money(revenue_str)
                price = parse_money(price_str)
                multiple = float(multiple_str.replace('x', '')) if 'x' in multiple_str else 0
                
                startups.append({
                    'name': name,
                    'url': 'https://trustmrr.com' + href,
                    'category': category,
                    'revenue': revenue,
                    'price': price,
                    'multiple': multiple
                })
                
    # Remove duplicates
    unique_startups = {}
    for s in startups:
        unique_startups[s['name']] = s
        
    startups_list = list(unique_startups.values())
    
    # Calculate some extra metrics for ranking
    for s in startups_list:
        # Avoid division by zero
        s['roi_monthly'] = s['revenue'] / s['price'] if s['price'] > 0 else 0
        s['months_to_recover'] = s['price'] / s['revenue'] if s['revenue'] > 0 else float('inf')
    
    # Sort by revenue (highest first) as a baseline for "keuntungannya gede"
    startups_list.sort(key=lambda x: x['revenue'], reverse=True)
    
    with open("startups.json", "w", encoding="utf-8") as f:
        json.dump(startups_list, f, indent=2)
        
    print(f"Extracted {len(startups_list)} unique startups.")
    
    # Let's print top 10 by highest revenue
    print("\nTop 10 Startups by Revenue:")
    for s in startups_list[:10]:
        print(f"- {s['name']} | Rev: ${s['revenue']:,.0f} | Price: ${s['price']:,.0f} | Cat: {s['category']} | ROI: {s['roi_monthly']:.2f} (mo: {s['months_to_recover']:.1f})")
        
    # Let's print top 5 "most potential/anti rugi" (High Revenue, reasonable recovery time < 36 months, low multiple)
    # Filter for startups with > $1000 revenue
    solid_startups = [s for s in startups_list if s['revenue'] > 1000 and s['months_to_recover'] < 60]
    solid_startups.sort(key=lambda x: x['months_to_recover'])
    
    print("\nTop 5 Most Potential (Fastest Recovery Time & >$1k Revenue):")
    for s in solid_startups[:5]:
        print(f"- {s['name']} | Rev: ${s['revenue']:,.0f} | Price: ${s['price']:,.0f} | Cat: {s['category']} | ROI: {s['roi_monthly']:.2f} (mo: {s['months_to_recover']:.1f})")

if __name__ == "__main__":
    extract_startups()
