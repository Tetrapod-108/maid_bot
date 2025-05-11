from google import genai
from google.genai import types
import datetime
import json

#import features.remind.remind
from features.gemini import history_repository
from features.multi_guild import guild_data_repository

# Gemini APIのラッパー
class GeminiChatService:
    # コンストラクタ
    def __init__(self, api_key: str, prompt_path: str, history_file_path: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt = f.read()
        self.meta_data = None
        self.model = model
        self.history_repo = history_repository.HistoryRepository(history_file_path)
        #self.guild_repo = multi_guild_repository.MultiGuildRepository(guild_file_path)
    
    # メタ情報とシステムメッセージ、ユーザーからのメッセージを渡して返答を生成
    def talk(self, guild_id, in_meta_data: str = None, system_msg: str = "", msg: str = ""):
        if in_meta_data == None:
            meta_data = f"{{\"meta_data\":[{{\"now_date\": {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}}}]}}"
        else:
            meta_data = in_meta_data
        fixed_system_msg = f"{{\"system_message\":\"{system_msg}\"}}"
        self.edit_history_path(guild_id=guild_id)
        chat = self.client.chats.create(model = self.model, config = types.GenerateContentConfig(temperature=1.7, system_instruction=meta_data+self.prompt), history=self.history_repo.load())
        #chat = self.client.chats.create(model = self.model, config = types.GenerateContentConfig(temperature=1.7), history=self.history_registory.load())
        #print(meta_data+fixed_system_msg+self.prompt+msg)
        try:
            res = chat.send_message(fixed_system_msg+msg)
            history = chat.get_history()
            self.history_repo.save(history)
            return res.text
        except:
            return "申し訳ございません。\nエラーが発生しているようですので、少々お待ち下さい。"

    def talk_for_diary(self, guild_id, in_meta_data: str = None, msg: str = ""):
        if in_meta_data == None:
            self.gen_meta_data()
        else:
            meta_data = in_meta_data
        system_msg = ""
        fixed_system_msg = f"{{\"system_message\":\"{system_msg}\"}}"
        self.edit_history_path(guild_id=guild_id)
        chat = self.client.chats.create(model = self.model, config = types.GenerateContentConfig(temperature=1.7, system_instruction=meta_data+self.prompt), history=self.history_repo.load())
        res = chat.send_message(fixed_system_msg+msg)
        history = chat.get_history()
        self.history_repo.save(history)
        return res.text

    # メタ情報を生成
    def gen_meta_data(self):
        meta_data = f"{{\"meta_data\":[{{\"now_date\": {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}}}]}}"
        self.meta_data = meta_data

    # ヒストリーファイルのパスに与えられたGuildのidを代入する
    def edit_history_path(self, guild_id):
        before  = self.history_repo.in_file_path
        after = before.replace("XXX", f"{guild_id}")
        self.history_repo.file_path = after

"""
from pathlib import Path

if __name__ == "__main__":
    client = genai.Client(api_key="")
    with open(f"{Path(__file__).parent/"analyze_prompt.md"}", "r", encoding="utf-8") as f:
        data = f.read()
    config = types.GenerateContentConfig(system_instruction=data)
    contents = "明日の天気は？"
    res = client.models.generate_content(model='gemini-2.0-flash', config=config, contents=contents)
    print(res.text)
"""