import json
from features.task_list import task

# Taskオブジェクトとjsonファイルを接続するユースケース
class TaskRepository():
    # コンストラクタ
    def __init__(self, file_path: str):
        self.in_file_path: str = file_path
        self.file_path: str = None
    
    # Taskオブジェクトをデータベース(jsonファイル)に追記
    def add(self, task: task.Task):
        with open(self.file_path, "r") as f:
            data:list = json.load(f)
        data.append(task.export_to_dict())
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    # 指定された名前のタスクを削除
    def remove(self, name: str):
        flag = 0
        with open(self.file_path, "r") as f:
            data:list = json.load(f)
        for i in data:
            if i["name"] == name:
                data.remove(i)
                flag = 1
        if flag == 1:
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=4)
        else:
            raise Exception

    # 全てのタスクを取得
    def get_all(self):
        with open(self.file_path, "r") as f:
            data:list = json.load(f)
        fixed_data = []
        for i in data:
            fixed_data.append(task.Task.import_from_dict(i))
        return fixed_data

    # taskファイルのパスに与えられたGuildのidを代入する
    def edit_task_path(self, guild_id):
        before  = self.in_file_path
        after = before.replace("XXX", f"{guild_id}")
        self.file_path = after