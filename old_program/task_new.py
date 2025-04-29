import json


# タスクのドメインクラス
class Task():
    # コンストラクタ
    def __init__(self, name: str = None, in_date: str = None, in_time: str = None):
        self.name: str = name
        self.date: str = in_date
        self.time: str = in_time
    
    # 適切な辞書型からインスタンスを作成
    @classmethod
    def import_from_dict(cls, data: dict) -> "Task":
        try:
            return cls(name = data["name"], in_date = data["date"], in_time = data["time"])
        except KeyError as e:
            raise

    # 情報を辞書型にエクスポート
    def export_to_dict(self) -> dict:
        return_dict = {"name": self.name, "date": self.date, "time": self.time}
        return return_dict
    
    # 情報を表示用にフォーマット
    def format_to_str(self) -> str:
        date = self.date
        time = self.time
        if self.date == None:
            date = ""
        if self.time == None:
            time = ""
        return f"{self.name}{date}{time}"


# Taskオブジェクトとjsonファイルを接続するユースケース
class TaskRepository():
    # コンストラクタ
    def __init__(self, file_path: str):
        self.file_path: str = file_path
    
    # Taskオブジェクトをデータベース(jsonファイル)に追記
    def add(self, task: Task):
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
            fixed_data.append(Task.import_from_dict(i))
        return fixed_data


"""
if __name__ == "__main__":
    #task = Task()
    #a = {"name": "テスト", "date": "2025-04-23", "time": None}
    #print(type(Task().import_from_dict(a)))
    #print(str(task.name)+str(task.date)+str(task.time))
    #print(type(task.date))

    task_list = TaskRepository(file_path=f"{Path(__file__).parent}/json/task.json")
    data = task_list.get_all()
    msg = ""
    for i in data:
        msg += f"・{i.format_to_str()}\n"
    print(f"{msg}のようなタスクがあります")
    print(f"{Path(__file__).parent}/json/task.json")
"""