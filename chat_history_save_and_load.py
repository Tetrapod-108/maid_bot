# chat_history_save_and_load.py

from typing import List, Any
import json
from google.generativeai.protos import Content, Part

def save_gemini_history_to_json(gemini_history: List[Any], filename: str) -> None:
    print("Saving gemini_history to JSON. Structure of gemini_history:")
    
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
        print(f"Successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")

def load_gemini_history_from_json(filename: str) -> List[Content]:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        print(f"Successfully loaded from {filename}. Structure of loaded data:")
        
        # JSONデータをContentオブジェクトに変換
        gemini_history = []
        for item in loaded_data:
            parts = [Part(text=part['text']) for part in item['parts']]
            content = Content(role=item['role'], parts=parts)
            gemini_history.append(content)
        
        return gemini_history
    except Exception as e:
        print(f"Error loading from JSON: {e}")
        return []