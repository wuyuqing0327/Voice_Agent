import requests

import requests

def call_retell_ai_model(user_input, api_key, model='voice-agent-model'):
    url = "https://api.retellai.com/model/predict"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "inputs": {
            "text": user_input
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.ok:
        return response.json().get('response_text')
    else:
        raise Exception(f"API Request failed: {response.text}")


# 示例调用（替换成你的实际API密钥和输入）
api_key = "YOUR_API_KEY"
user_input = "Hello, can you help me schedule an appointment?"
response_text = call_retell_ai_model(user_input, api_key)
print(response_text)
