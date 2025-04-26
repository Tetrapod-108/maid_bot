from google.genai import types
import json


# chatのhistoryをjsonに保存するためのユースケース
class HistoryRegistory:
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