import datetime
import json
from pathlib import Path

import gemini

# 関数: remind_task
# list_onlyがTrueの時、文を整えた状態でタスクリストを返す
# Falseの時はタスクリストのみを返す
def remind_task(list_only: bool, now = None):
    if now != None:
        now_date = now.strftime("%m月%d日%H:%M")
    with open(f"{Path(__file__).parent}/json/task.json") as f:
        data = json.load(f)
    if len(data) == 0:
        res = "タスク無し"
        if list_only == False:
            res = gemini.talk(f"[システム: 現在の時間:{now_date} 注意: 各文の間に1行空ける必要はありません] マスターへの時間に適した挨拶、簡単な気遣いの言葉、という順でマスターにとくに予定がないことを通知してください。")
        return res
    task_str = ""
    for i in data:
        str_date = str(i["date"])
        str_time = str(i["time"])
        if i["date"] == None:
            str_date = ""
        if i["time"] == None:
            str_time = ""    
        task_str = f"・{i["name"]}{str_date}{str_time}\n" + task_str
    res = task_str
    if list_only == False:
        res = gemini.talk(f"「{task_str}」のようなタスクがあります。マスターへの挨拶、箇条書きで書いたタスクの一覧、内容のまとめ、という流れでマスターにタスクをリマインドしてください。今は{now_date}なので、適した挨拶、注意をしてください。")
    return res


# 関数: add_task
# タスクをリストに追加する
def add_task(name: str, date: str = None, time: str = None):
    with open(f"{Path(__file__).parent}/json/task.json") as f:
        data:list = json.load(f)
    data.append({"name":name, "date":date, "time":time})
    with open(f"{Path(__file__).parent}/json/task.json", "w") as f:
        json.dump(data, f, indent=4)
    res = gemini.talk(f"「{name}」のタスクをリストに追加してください")
    return res

# 関数: remove_task
# 名前を指定したタスクをリストから削除する
def remove_task(name: str):
    flag = 0
    with open(f"{Path(__file__).parent}/json/task.json") as f:
        data:list = json.load(f)
    for i in data:
        if i["name"] == name:
            data.remove(i)
            flag = 1
    if flag == 1:
        with open(f"{Path(__file__).parent}/json/task.json", "w") as f:
            json.dump(data, f, indent=4)
        return gemini.talk(f"「{name}」のタスクが終わったよ")
    else:
        return gemini.talk("マスターにされた指示が間違っていることを伝えてください", False)

if __name__ == "__main__":
    pass