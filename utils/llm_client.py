import os
import re
import time
from dotenv import load_dotenv
from openai import OpenAI, PermissionDeniedError, RateLimitError

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-isi-openai-key-anda-disini")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

FALLBACK_MODELS = [
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
    "qwen1.5-110b-chat",
    "qwen1.5-72b-chat",
    "qwen1.5-32b-chat",
    "qwen1.5-14b-chat",
    "qwen1.5-7b-chat",
    "qwen3.6-flash"
]

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

class LLMClient:
    @staticmethod
    def query(prompt, require_json=False, extract_code_block=False):
        for model_name in FALLBACK_MODELS:
            print(f"     [>] Memanggil AI ({model_name})...")
            try:
                response_format = {"type": "json_object"} if require_json else None
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    response_format=response_format
                )
                
                content = response.choices[0].message.content.strip()
                
                if extract_code_block and not require_json and content != "PERFECT":
                    match = re.search(r'```(?:tsx|typescript|ts|javascript|js|json)?\n(.*?)\n```', content, re.DOTALL)
                    if match:
                        content = match.group(1).strip()
                    elif content.startswith("```"):
                        content = content.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
                
                return content.strip()
                
            except PermissionDeniedError:
                print(f"     [X] Error 403 ({model_name}). Melompat ke cadangan...")
                continue
            except RateLimitError:
                print(f"     [X] Error 429 ({model_name}). Melompat ke cadangan...")
                time.sleep(2)
                continue
            except Exception as e:
                print(f"     [X] Error tak terduga ({model_name}): {e}")
                continue
                
        print("[!!!] FATAL ERROR: Semua model gagal!")
        return ""
