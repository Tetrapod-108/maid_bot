from google import genai
from google.genai import types
import json
from pathlib import Path

import config.key as key

# Gemini APIのラッパー
class GeminiChatService:
    # コンストラクタ
    def __init__(self, api_key: str, model: str, prompt: str, history_file_path: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        self.prompt = prompt
        self.model = model
        self.history_registory = HistoryRepository(history_file_path)
    
    # メタ情報とシステムメッセージ、ユーザーからのメッセージを渡して返答を生成
    def talk(self, metadata: str, system_msg: str = "", msg: str = ""):
        #print(metadata+system_msg+self.prompt)
        #chat = self.client.chats.create(model = self.model, config = types.GenerateContentConfig(temperature=1.7, system_instruction=metadata+system_msg+self.prompt), history=self.history_registory.load())
        chat = self.client.chats.create(model = self.model, config = types.GenerateContentConfig(temperature=1.7), history=self.history_registory.load())
        res = chat.send_message(metadata+system_msg+self.prompt)
        history = chat.get_history()
        self.history_registory.save(history)
        return res.text
    

# chatのhistoryをjsonに保存するためのユースケース
class HistoryRepository:
    # コンストラクタ
    def __init__(self, file_path: str):
        self.file_path = file_path

    # historyをjsonに保存
    def save(self, history: list):
        # Contentオブジェクトから必要な情報を抽出
        serializable_history = [
            {
                "role": item.role,
                "parts": [
                    {"text": part.text} if hasattr(part, 'text') else part
                    for part in item.parts
                ]
            }
            for item in history
        ]
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise

    # historyをjsonからロード
    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)   
            # JSONデータをContentオブジェクトに変換
            gemini_history = []
            for item in loaded_data:
                parts = [types.Part(text=part['text']) for part in item['parts']]
                content = types.Content(role=item['role'], parts=parts)
                gemini_history.append(content)
            return gemini_history
        except Exception as e:
            raise
    

if __name__ == "__main__":
    with open(f"{Path(__file__).parent}/json/system_prompt_new.json", "r", encoding="utf-8") as f:
        PROMPT = f.read()
    gemini = GeminiChatService(api_key=key.GEMINI_API_KEY, model="gemini-2.0-flash", prompt=PROMPT, history_file_path=f"{Path(__file__).parent}/json/history_new.json")
    print(gemini.talk(metadata = "{metadata:[{'now_date':'2025-04-24 0:58'}]}", system_msg="{system_message:'あなたの自己紹介をしてください'}"))
    
    
    

