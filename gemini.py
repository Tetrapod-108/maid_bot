import google.generativeai as genai
from google.generativeai.protos import Content, Part
from typing import List, Any
import json
from pathlib import Path

import key

with open(f"{Path(__file__).parent}/json/history.json", "r") as f:
        PROMPT = f.read()
CONFIG = genai.types.GenerationConfig(temperature=1.7)


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


def talk(msg: str, take_over_history: bool = True):
    genai.configure(api_key=key.GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name = "gemini-2.0-flash", 
                                  generation_config = CONFIG,
                                  system_instruction = PROMPT)
    history = load_gemini_history_from_json(f"{Path(__file__).parent}/json/history.json")
    chat = model.start_chat(history = history)
    res = chat.send_message(content = msg, generation_config = CONFIG)
    history = chat.history
    if take_over_history == True:
        save_gemini_history_to_json(history, f"{Path(__file__).parent}/json/history.json")
    return res.text

if __name__ == "__main__":
    now = "17:42"
    task_list = "ミーティング、名刺デザイン作成"
    msg = f"[システム: 時間:{now} 天気:晴れ 気温:12℃]「{task_list}」のようなタスクがあります。マスターへの簡単な挨拶、簡単な気遣いの一文、タスクについての簡単なまとめ、という流れでマスターに話してください。与えられた情報に適した挨拶、注意喚起をしてください。また、文の間に1行空けないでください。"
    print(talk(msg, False))
    pass
