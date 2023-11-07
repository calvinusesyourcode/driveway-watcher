import base64
import requests
import os

i_token_cost = 0.01/1000
o_token_cost = 0.03/1000

def encode_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def describe_image(image_path):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": "DescribeImage|10WordsOrLess"
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{encode_image_as_base64(image_path)}"
                }
            }
            ]
        }
        ],
        "max_tokens": 20,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers,json=payload).json()
    
    cost = (response['usage']['prompt_tokens'] * i_token_cost) + (response['usage']['completion_tokens'] * o_token_cost)
    text = response['choices'][0]['message']['content']
    print(f"${cost}: {text}")

describe_image("motion_20231106_165302.png")