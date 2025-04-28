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
        return f"{self.name} {date}{time}"
