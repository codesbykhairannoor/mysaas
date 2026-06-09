import requests
import json

def test_models():
    api_key = "sk-ws-H.IILIRY.oTvU.MEUCIDaoFk8Ww5HPTEt2AtyyXYmHaz6hgTp9gEgf0vord6ApAiEArIwkxfLAgnKPhrLlHhcCvo-HoRJxOhZrz1jIupxBV7U"
    
    # Test multiple Alibaba Cloud Qwen models
    models_to_test = [
        "qwen-turbo",
        "qwen-plus",
        "qwen-max",
        "qwen-turbo-latest",
        "qwen2.5-72b-instruct",
        "qwen2.5-32b-instruct",
        "qwen2.5-14b-instruct",
        "qwen2.5-7b-instruct",
        "qwen2.5-3b-instruct",
        "qwen2.5-1.5b-instruct",
        "qwen2.5-0.5b-instruct",
        "qwen-coder-turbo",
        "qwen-coder-plus",
        "qwen2.5-coder-32b-instruct",
        "qwen2.5-coder-14b-instruct",
        "qwen2.5-coder-7b-instruct",
    ]
    
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("=" * 70)
    print("TESTING ALIBABA CLOUD DASHSCOPE MODELS")
    print("=" * 70)
    
    working_models = []
    
    for model in models_to_test:
        payload = {
            "model": model,
            "input": {
                "messages": [
                    {"role": "user", "content": "Say exactly: Model is working!"}
                ]
            },
            "parameters": {
                "max_tokens": 50,
                "temperature": 0.1
            }
        }
        
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                result = resp.json()
                output = result.get("output", {}).get("text", "")
                print(f"✅ {model} — WORKING! Response: {output.strip()[:80]}")
                working_models.append(model)
            elif resp.status_code == 404:
                print(f"❌ {model} — Model not found")
            else:
                err_msg = resp.json().get("output", {}).get("text", resp.text[:200]) if resp.text else "No response"
                print(f"⚠️  {model} — Error {resp.status_code}: {err_msg}")
        except Exception as e:
            print(f"⚠️  {model} — Connection error: {str(e)[:80]}")
    
    print("\n" + "=" * 70)
    print(f"WORKING MODELS ({len(working_models)}):")
    for m in working_models:
        print(f"  - {m}")
    print("=" * 70)

if __name__ == "__main__":
    test_models()