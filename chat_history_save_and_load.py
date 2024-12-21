# chat_history_save_and_load.py

from typing import List, Any
import json
from google.generativeai.protos import Content, Part

def save_gemini_history_to_json(gemini_history: List[Any], filename: str) -> None:
    
    # Contentオブジェクトから必要な情報を抽出
    serializable_history = [
        {
            "role": item.role,
            "parts": [
                {"text": part.text} if hasattr(part, 'text') else part
                for part in item.parts
            ]
        }
        for item in gemini_history
    ]
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pass

def load_gemini_history_from_json(filename: str) -> List[Content]:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        # JSONデータをContentオブジェクトに変換
        gemini_history = []
        for item in loaded_data:
            parts = [Part(text=part['text']) for part in item['parts']]
            content = Content(role=item['role'], parts=parts)
            gemini_history.append(content)
        
        return gemini_history
    except Exception as e:
        return []