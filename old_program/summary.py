import google.generativeai as genai
#from google import genai
from google.generativeai.protos import Content, Part
from typing import List, Any
import json
from pathlib import Path

import config.key as key

CONFIG = genai.types.GenerationConfig(temperature=0.1)
PROMPT = "アシスタントAIとそのマスターの会話記録を示します。LLMのヒストリーに渡してやりとりの記憶を引き継ぐために、会話の内容を4000字以下に整理してください。LLMが認識しやすい書式で出力してください\n"

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
    genai.configure(api_key=key.GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name = "gemini-2.5-pro-exp-03-25", 
                                  generation_config = CONFIG,
                                  system_instruction = PROMPT)
    with open("json/history.json", "r") as f:
        data = f.read()
    response = model.generate_content(PROMPT+str(data))
    print(response.text)