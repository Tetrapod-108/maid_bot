import datetime
import re


# リマインドのドメインクラス
class Remind():
    # コンストラクタ
    def __init__(self, name: str, date: datetime.datetime):
        self.name = name
        self.date: datetime.datetime = date

    # 適切な辞書型からインスタンスを作成
    @classmethod
    def import_from_dict(cls, data: dict) -> "Remind":
        try:
            date_format = "%Y-%m-%d %H:%M"
            return cls(name = data["name"], date = datetime.datetime.strptime(data["date"], date_format))
        except KeyError as e:
            raise
    
    # 情報を辞書型にエクスポート
    def export_to_dict(self) -> dict:
        date_format = "%Y-%m-%d %H:%M"
        return_dict = {"name": self.name, "date": self.date.strftime(date_format)}
        return return_dict

    # 時刻情報をin_dateに基づいて編集
    def edit_date(self, in_date: str):
        day = 0
        hour = 0
        minute = 0
        flag = 0
        format1_1 = r"([0-9]{1,2})d([0-9]{1,2})h([0-9]{1,2})m"
        format1_2 = r"([0-9]{1,2})h([0-9]{1,2})m"
        format1_3 = r"([0-9]{1,2})d([0-9]{1,2})h"
        format1_4 = r"([0-9]{1,2})d([0-9]{1,2})m"
        format1_5 = r"([0-9]{1,2})m"
        format1_6 = r"([0-9]{1,2})h"
        format1_7 = r"([0-9]{1,2})d"
        format2 = r"([0-9]{1,2}):([0-9]{1,2})"
        if re.compile(format1_1).match(in_date) != None:
            f1_1 = re.compile(format1_1).match(in_date)
            day = int(f1_1.groups()[0])
            hour = int(f1_1.groups()[1])
            minute = int(f1_1.groups()[2])
        elif re.compile(format1_2).match(in_date) != None:
            f1_2 = re.compile(format1_2).match(in_date)
            hour = int(f1_2.groups()[0])
            minute = int(f1_2.groups()[1])
        elif re.compile(format1_3).match(in_date) != None:
            f1_3 = re.compile(format1_3).match(in_date)
            day = int(f1_3.groups()[0])
            hour = int(f1_3.groups()[1])
        elif re.compile(format1_4).match(in_date) != None:
            f1_4 = re.compile(format1_4).match(in_date)
            day = int(f1_4.groups()[0])
            minute = int(f1_4.groups()[1])
        elif re.compile(format1_5).match(in_date) != None:
            f1_5 = re.compile(format1_5).match(in_date)
            minute = int(f1_5.groups()[0])
        elif re.compile(format1_6).match(in_date) != None:
            f1_6 = re.compile(format1_6).match(in_date)
            hour = int(f1_6.groups()[0])
        elif re.compile(format1_7).match(in_date) != None:
            f1_7 = re.compile(format1_7).match(in_date)
            day = int(f1_7.groups()[0])
        elif re.compile(format2).match(in_date) != None:
            f2 = re.compile(format2).match(in_date)
            set_hour = int(f2.groups()[0])
            set_minute = int(f2.groups()[1])
            if set_hour > 23 or set_minute > 59:
                raise Exception
            delta_day = 0
            if self.date.hour > set_hour:
                delta_day = 1
            if self.date.hour > set_hour or (self.date.hour == set_hour and self.date.minute > set_minute):
                delta_day = 1
            delta = datetime.timedelta(days = delta_day, hours = hour, minutes = minute)
            set_date = self.date + delta
            set_date = set_date.replace(hour = set_hour)
            set_date = set_date.replace(minute = set_minute)
            self.date = set_date
            flag = 1
        else:
            raise Exception
        if flag == 0:
            delta = datetime.timedelta(days = day, hours = hour, minutes = minute)
            set_date = self.date + delta
            self.date = set_date
    
    # dateをstrに直して返す
    def format_date(self) -> str:
        date_format = "%Y-%m-%d %H:%M"
        return self.date.strftime(date_format)
