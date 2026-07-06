import os
import requests
import sys

def list_models(api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        print("Model yang tersedia untuk API Key Anda:")
        for model in data.get("models", []):
            if "generateContent" in model.get("supportedGenerationMethods", []):
                print(f"- {model['name']}")
    else:
        print(f"Error: {resp.status_code}, {resp.text}")

if __name__ == "__main__":
    api_key = sys.argv[1] if len(sys.argv) > 1 else None
    if not api_key:
        print("Harap masukkan API Key sebagai argumen.")
    else:
        list_models(api_key)
