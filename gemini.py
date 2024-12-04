import google.generativeai as genai

import chat_history_save_and_load as chsl
from key import key


PROMPT = "長く屋敷に仕えるメイド。口調は敬語だが堅苦しくはない。クールな印象を受けるが根は優しい。様々な分野に精通していて博識。主人のことを「マスター」と呼ぶ。「!」は使わない。文の最後に改行する。冗長な表現はしない。"
CONFIG = genai.types.GenerationConfig(temperature=2.0)

def talk(msg: str):
    genai.configure(api_key=key.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "model", "parts": PROMPT}
        ]
    )
    res = chat.send_message(content = msg, generation_config = CONFIG)
    history = chat.history
    print(history)
    return res.text