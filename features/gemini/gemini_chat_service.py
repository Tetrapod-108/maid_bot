from google import genai
from google.genai import types

import history_registory


# Gemini APIのラッパー
class GeminiChatService:
    # コンストラクタ
    def __init__(self, api_key: str, model: str, prompt: str, history_file_path: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        self.prompt = prompt
        self.model = model
        self.history_registory = history_registory.HistoryRegistory(history_file_path)
    
    # メタ情報とシステムメッセージ、ユーザーからのメッセージを渡して返答を生成
    def talk(self, metadata: str, system_msg: str = "", msg: str = ""):
        chat = self.client.chats.create(model = self.model, config = types.GenerateContentConfig(temperature=1.7, system_instruction=metadata+system_msg+self.prompt), history=self.history_registory.load())
        res = chat.send_message(msg)
        history = chat.get_history()
        self.history_registory.save(history)
        return res.text