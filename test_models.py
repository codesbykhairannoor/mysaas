import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-isi-openai-key-anda-disini":
    print("API Key tidak ditemukan atau masih default!")
    exit(1)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

models_to_test = [
    "qwen-turbo",
    "qwen-plus",
    "qwen-max",
    "qwen-long",
    "qwen-turbo-latest",
    "qwen-plus-latest",
    "qwen-max-latest",
    "qwen2.5-72b-instruct",
    "qwen2.5-32b-instruct",
    "qwen2.5-14b-instruct",
    "qwen2.5-7b-instruct",
    "qwen2.5-coder-32b-instruct",
    "qwen1.5-110b-chat",
    "qwen1.5-72b-chat",
    "qwen1.5-32b-chat",
    "qwen1.5-14b-chat",
    "qwen1.5-7b-chat",
    "qwen3.6-flash",
    "qwen-vl-plus",
    "qwen-vl-max"
]

print("Mulai pengujian model aktif di Alibaba Cloud DashScope...\n")

active_models = []
dead_models = []

for model in models_to_test:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print(f"[+] AKTIF: {model}")
        active_models.append(model)
    except Exception as e:
        err_msg = str(e).split('\n')[0]
        print(f"[-] GAGAL: {model} -> {err_msg[:80]}")
        dead_models.append(model)

print("\n=== RINGKASAN ===")
print(f"Total Aktif: {len(active_models)}")
print("Model yang siap digunakan:")
for m in active_models:
    print(f"- {m}")
