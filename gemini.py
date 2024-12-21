import google.generativeai as genai
from google.generativeai.protos import Content, Part
from typing import List, Any
import json
from pathlib import Path

from key import key

PROMPT = \
"長く屋敷に仕えるメイド。口調は温かみのある敬語。様々な分野に精通していて博識。主人のことを「マスター」と呼ぶ。「!」は使わない。文の最後に改行する。口調の例:「お疲れ様です、マスター。本日は気温差が大きいため、お体に気を付けてお過ごしくださいませ。」"
CONFIG = genai.types.GenerationConfig(temperature=1.0)

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
    model = genai.GenerativeModel("gemini-1.5-flash")
    history = load_gemini_history_from_json(f"{Path(__file__).parent}/json/history.json")
    chat = model.start_chat(history = history)
    res = chat.send_message(content = msg, generation_config = CONFIG)
    history = chat.history
    if take_over_history == True:
        save_gemini_history_to_json(history, f"{Path(__file__).parent}/json/history.json")
    return res.text

if __name__ == "__main__":
    data = [{"id":0,"name":"数学課題提出", "date":"12月13日", "time":"17:00"},
            {"id":1,"name":"ミーティング", "date":"12月14日", "time":"17:00"}]
    task_str = ""
    for i in range(len(data)):
        task_str = f"{data[i]["name"]}{data[i]["date"]}{data[i]["time"]}," + task_str
    #msg = f"「{task_str}」のようなタスクがあります。マスターへの挨拶、箇条書きで書いたタスクの一覧、気遣いの言葉、という流れでマスターに予定をリマインドしてください。今は12月13日9:00なので、適した挨拶、注意をしてください"
    msg = "「自転車メンテナンス」のタスクをリストに追加しておいてくれるかな？"
    msg = "マスターに指示が間違っていることを伝えてください"
    print(msg)
    print(talk(msg))
    #print(talk("こんばんは"))
