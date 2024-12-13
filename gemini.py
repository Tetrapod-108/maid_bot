import google.generativeai as genai

import chat_history_save_and_load as chsl
from key import key


PROMPT = \
"長く屋敷に仕えるメイド。口調は温かみのある敬語。様々な分野に精通していて博識。主人のことを「マスター」と呼ぶ。「!」は使わない。文の最後に改行する。口調の例:「お疲れ様です、マスター。本日は気温差が大きいため、お体に気を付けてお過ごしくださいませ。」"
CONFIG = genai.types.GenerationConfig(temperature=2.0)

def talk(msg: str, take_over_history: bool = True):
    genai.configure(api_key=key.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    history = chsl.load_gemini_history_from_json("history.json")
    chat = model.start_chat(history = history)
    res = chat.send_message(content = msg, generation_config = CONFIG)
    history = chat.history
    if take_over_history == True:
        chsl.save_gemini_history_to_json(history, "history.json")
    return res.text

data = [{"id":0,"name":"数学課題提出", "date":"12月13日", "time":"17:00"},
        {"id":1,"name":"ミーティング", "date":"12月14日", "time":"17:00"}]
task_str = ""
for i in range(len(data)):
    task_str = f"{data[i]["name"]}{data[i]["date"]}{data[i]["time"]}," + task_str
msg = f"主人に以下のようなタスクがあることを、箇条書きで伝えてください。今は12月13日13:00です。「{task_str}」"
print(msg)
print(talk(msg, False))