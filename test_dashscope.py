import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

models_to_test = [
    "qwen-turbo",
    "qwen-plus",
    "qwen-max",
    "qwen-flash",
    "qwen-long",
    "qwen-turbo-latest",
    "qwen2.5-7b-instruct",
    "qwen2.5-14b-instruct",
    "qwen2.5-32b-instruct",
    "qwen2.5-72b-instruct"
]

print("=== MENGUJI KONEKSI MODEL ALIBABA ===")
for model in models_to_test:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print(f"[SUCCESS] {model} -> CONNECTED!")
    except Exception as e:
        error_str = str(e)
        if "403" in error_str:
            print(f"[FAILED]  {model} -> 403 Access Denied")
        elif "404" in error_str:
            print(f"[FAILED]  {model} -> 404 Model Not Found")
        else:
            print(f"[FAILED]  {model} -> {e}")

print("=== SELESAI ===")
