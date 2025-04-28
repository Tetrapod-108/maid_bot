import json
import datetime
from features.remind import remind


# Remindオブジェクトとjsonファイルを接続するユースケース
class RemindRepository():
    # コンストラクタ
    def __init__(self, file_path: str):
        self.file_path = file_path

    # jsonにリマインド情報を追加
    def add(self, remind: remind.Remind):
        with open(self.file_path, "r") as f:
            data:list = json.load(f)
        data.append(remind.export_to_dict())
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    # jsonから特定のリマインド情報を削除
    def remove(self, remind: remind.Remind):
        flag = 0
        with open(self.file_path, "r") as f:
            data:list = json.load(f)
        for i in data:
            remind_dict = remind.export_to_dict() 
            if i == remind_dict:
                data.remove(i)
            flag = 1
        if flag == 1:
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=4)
        else:
            return
        
    # dateに合致するリマインド情報がjsonにあるかを検索
    def search(self, name: str = None, date: datetime.datetime = None) -> list:
        return_list = []
        with open(self.file_path, "r") as f:
            data:list = json.load(f)
        for i in data:
            if i["name"] == name or i["date"] == date.strftime("%Y-%m-%d %H:%M"):
                return_list.append(remind.Remind.import_from_dict(i))
        return return_list