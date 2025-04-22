import google.generativeai as genai
#from google import genai
from google.generativeai.protos import Content, Part
from typing import List, Any
import json
from pathlib import Path

import key

CONFIG = genai.types.GenerationConfig(temperature=1.7)
PROMPT = "アシスタントAIとそのマスターの会話記録を示します。どんな出来事があったのか分かるように2000文字ほどに要約してください\n"

def summary(msg: str):
    genai.configure(api_key=key.GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name = "gemini-2.0-flash", 
                                  generation_config = CONFIG,
                                  system_instruction = PROMPT)
    chat = model.start_chat(history = history)
    res = chat.send_message(content = msg, generation_config = CONFIG)
    history = chat.history
    return res.text

if __name__ == "__main__":
    client = genai.Client(api_key=key.GEMINI_API_KEY)
    with open("json/history.json", "r") as f:
        data = f.read()
    response = client.models.generate_content(
    model="gemini-2.0-pro",
    contents=[data]
    )
    print(response.text)