import requests
import re
import json

API_KEY = "sk-ws-H.IILIRY.oTvU.MEUCIDaoFk8Ww5HPTEt2AtyyXYmHaz6hgTp9gEgf0vord6ApAiEArIwkxfLAgnKPhrLlHhcCvo-HoRJxOhZrz1jIupxBV7U"

print("=" * 70)
print("STEP 1: FETCH ALIBABA CLOUD DOCUMENTATION PAGE")
print("=" * 70)

r = requests.get("https://api.alibabacloud.com/document", timeout=15, headers={"User-Agent": "Mozilla/5.0"})
print(f"Status: {r.status_code}")

# Find all API product links
link_pattern = re.compile(r'href=["\']([^"\']*?)["\']')
all_links = link_pattern.findall(r.text)

# Find links related to AI, LLM, Model Studio
ai_links = []
for link in all_links:
    l = link.lower()
    if any(kw in l for kw in ["ai", "llm", "model-studio", "dashscope", "qwen", "text-generation", "tongyi"]):
        ai_links.append(link)

print(f"\nFound {len(ai_links)} AI-related links:")
for l in ai_links[:20]:
    print(f"  - {l}")

print("\n" + "=" * 70)
print("STEP 2: CHECK ALIBABA CLOUD AI MODEL STUDIO API")
print("=" * 70)

# Try the international Model Studio endpoint
endpoints = [
    # OpenAI compatible format
    {"url": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions", "name": "DashScope Intl (OpenAI format)"},
    # Original generation endpoint
    {"url": "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation", "name": "DashScope Intl (native)"},
    # Try with sk-ws prefix - maybe it's for a different service
    {"url": "https://api.alibabacloud.com/v1/chat/completions", "name": "Alibaba Cloud API (generic)"},
    # Try model-studio subdomain
    {"url": "https://model-studio.aliyuncs.com/v1/chat/completions", "name": "Model Studio"},
    # Try with region
    {"url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "name": "DashScope CN (OpenAI format)"},
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

for ep in endpoints:
    try:
        data = {
            "model": "qwen-turbo",
            "messages": [{"role": "user", "content": "Say: hello"}],
            "max_tokens": 10
        }
        resp = requests.post(ep["url"], headers=headers, json=data, timeout=10)
        print(f"\n[{ep['name']}]")
        print(f"  URL: {ep['url']}")
        print(f"  Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"  ✅ WORKING! Response: {resp.text[:200]}")
        else:
            print(f"  Response: {resp.text[:200]}")
    except Exception as e:
        print(f"\n[{ep['name']}] Error: {str(e)[:100]}")

print("\n" + "=" * 70)
print("STEP 3: CHECK IF KEY IS FOR ALIBABA CLOUD (NOT DASHSCOPE)")
print("=" * 70)

# Try different auth methods
auth_tests = [
    {"name": "x-api-key header", "headers": {"X-API-Key": API_KEY, "Content-Type": "application/json"}},
    {"name": "API-Key header", "headers": {"API-Key": API_KEY, "Content-Type": "application/json"}},
    {"name": "x-dashscope-authorization", "headers": {"X-DashScope-Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}},
    {"name": "query param ?api_key", "url_suffix": f"?api_key={API_KEY}"},
]

base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"
data = {"model": "qwen-turbo", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5}

for test in auth_tests:
    try:
        url = base_url + test.get("url_suffix", "")
        resp = requests.post(url, headers=test["headers"], json=data, timeout=10)
        print(f"\n[{test['name']}] Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"  ✅ WORKING!")
        else:
            print(f"  {resp.text[:150]}")
    except Exception as e:
        print(f"\n[{test['name']}] Error: {str(e)[:80]}")

print("\nDone!")