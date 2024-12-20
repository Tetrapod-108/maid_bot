import datetime
import json

import gemini

def remind_task(now_date: datetime.datetime):
    with open("json/task.json") as f:
        data = json.load(f)
    #print(data)
    if len(data) == 0:
        res = gemini.talk(f"マスターへの挨拶、簡単な気遣いの言葉、という順でマスターにとくに予定がないことを通知してください。今日は{now_date}なので、適した挨拶をしてください。")
        return res
    task_str = ""
    for i in range(len(data)):
        task_str = f"{data[i]["name"]}{data[i]["date"]}{data[i]["time"]}," + task_str
    res = gemini.talk(f"「{task_str}」のようなタスクがあります。マスターへの挨拶、箇条書きで書いたタスクの一覧、簡単な気遣いの一文、という流れでマスターに予定をリマインドしてください。今は{now_date}なので、適した挨拶、注意をしてください")
    return res

def add_task():
    with open("json/task.json") as f:
        data = json.load(f)
    print(data)
    print(data[0]["id"])

print(remind_task("12月20日14:00"))