import datetime
import json

import gemini

def remind_task(input_date: datetime.datetime):
    now_date = input_date.strftime("%m月%d日%H:%M")
    with open("json/task.json") as f:
        data = json.load(f)
    if len(data) == 0:
        res = gemini.talk(f"マスターへの挨拶、簡単な気遣いの言葉、という順でマスターにとくに予定がないことを通知してください。今は{now_date}なので、適した挨拶をしてください。")
        return res
    task_str = ""
    for i in range(len(data)):
        task_str = f"{data[i]["name"]}{data[i]["date"]}{data[i]["time"]}," + task_str
    res = gemini.talk(f"「{task_str}」のようなタスクがあります。マスターへの簡単な挨拶、箇条書きで書いたタスクの一覧、簡単な気遣いの一文、という流れでマスターに予定をリマインドしてください。今は{now_date}なので、適した挨拶、注意をしてください。また、文の間に1行空けないでください")
    return res

def add_task(name: str, date: str, time: str):
    with open("json/task.json") as f:
        data:list = json.load(f)
    data.append({"name":name, "date":date, "time":time})
    with open("json/task.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    add_task("線形代数課題", "12月24日", "17:00")
    print(remind_task(datetime.datetime.now()))