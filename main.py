import google.generativeai as genai

# APIKEY
key = "REMOVED"

genai.configure(api_key=key)

instraction = "長く屋敷に仕えるメイド。口調は敬語だが堅苦しくはない。クールな印象を受けるが根は優しい。様々な分野に精通していて博識。主人のことを「マスター」と呼ぶ。「!」は使わない。文の最後に改行する。冗長な表現はしない。"
config = genai.types.GenerationConfig(temperature=2.0)

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "model", "parts": instraction}
    ]
)

weather = "晴れ"
max_temp = 14
min_temp = 4
response = chat.send_message(f"主人に明日の天気が{weather}で、最高気温{max_temp}度、最低気温{min_temp}度であることを気遣いの言葉とともに伝えてください。天気と気温には太字をかけてください",generation_config = config)
print(response.text)
response = chat.send_message("なるほど、かなり寒いんだね", generation_config = config)
print(response.text)
response = chat.send_message("主人に17:00にアルバイトがある事をリマインドしてください", generation_config = config)
print(response.text)
task = ["美容室", "課題提出", "打合せ"]
response = chat.send_message(f"主人に今日のタスク、{task}を箇条書きでリマインドしてください", generation_config = config)
print(response.text)
msg = "今日は雨だったよ。洗濯物とりこんでて良かった..."
response = chat.send_message(f"「{msg}」への反応を絵文字1文字で表してください", generation_config = config)
print(response.text)