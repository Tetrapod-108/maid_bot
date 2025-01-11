import datetime
import json
from pathlib import Path

import gemini

# 関数: remind_task
# 文を整えた状態でタスクリストを表示する
def remind_task(input_date: datetime.datetime):
    now_date = input_date.strftime("%m月%d日%H:%M")
    with open(f"{Path(__file__).parent}/json/task.json") as f:
        data = json.load(f)
    if len(data) == 0:
        res = "タスク無し"
        return res
        #res = gemini.talk(f"マスターへの挨拶、簡単な気遣いの言葉、という順でマスターにとくに予定がないことを通知してください。今は{now_date}なので、適した挨拶をしてください。")
    task_str = ""
    for i in data:
        task_str = f"{i["name"]}{i["date"]}{i["time"]}," + task_str
    res = task_str
    #res = gemini.talk(f"「{task_str}」のようなタスクがあります。マスターへの簡単な挨拶、箇条書きで書いたタスクの一覧、簡単な気遣いの一文、という流れでマスターに予定をリマインドしてください。今は{now_date}なので、適した挨拶、注意をしてください。また、文の間に1行空けないでください")
    return res


# 関数: add_task
# タスクをリストに追加する
def add_task(name: str, date: str = None, time: str = None):
    with open(f"{Path(__file__).parent}/json/task.json") as f:
        data:list = json.load(f)
    data.append({"name":name, "date":date, "time":time})
    with open(f"{Path(__file__).parent}/json/task.json", "w") as f:
        json.dump(data, f, indent=4)
    res = gemini.talk(f"「{name}」のタスクをリストに追加してくれる？")
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