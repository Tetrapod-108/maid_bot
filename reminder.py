import io
import os
import re
import json
from datetime import datetime
from datetime import timedelta
from typing import Union
from pathlib import Path

import gemini


# クラス: リマインドのデータ
class Reminder:
    # コンストラクタ
    def __init__(self, in_user: str, in_date: Union[datetime, str], in_guild: str, in_ch: str, in_msg: str, date_calc = False):
        self.user = in_user # メンバ: user: リマインドを作成したユーザーの名前
        self.date = "" # メンバ: date: リマインドする日時
        self.guild = in_guild # メンバ: guild: リマインドするDiscordサーバー
        self.channel = in_ch # メンバ: channel: リマインドするチャンネル
        self.message = in_msg # メンバ: message: リマインドするメッセージ

        # 受け取ったin_dateを加工するか、そのまま使うか
        if date_calc == True:
            day = 0
            hour = 0
            minute = 0
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
                    self.user = "-1"
                    return
                now = datetime.now()
                if now.hour > set_hour:
                    day = 1
                delta = timedelta(days = day, hours = hour, minutes = minute)
                set_date = now + delta
                set_date = set_date.replace(hour = set_hour)
                set_date = set_date.replace(minute = set_minute)
                self.date = set_date.strftime("%Y-%m-%d %H:%M")
                return
            else:
                self.user = "-1"
                return
            now = datetime.now()
            delta = timedelta(days = day, hours = hour, minutes = minute)
            set_date = now + delta
            self.date = set_date.strftime("%Y-%m-%d %H:%M")
            
        elif date_calc == False:
            if type(in_date) is datetime:
                now = datetime.now()
                if now > in_date:
                    self.user = "-1"
                    return
                self.date = in_date.strftime("%Y-%m-%d %H:%M")
            elif type(in_date) is str:
                format = r"([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]{1,2}):([0-9]{1,2})"
                repatter = re.compile(format)
                result = repatter.match(in_date)
                year = int(result.groups()[0])
                month = int(result.groups()[1])
                day = int(result.groups()[2])
                hour = int(result.groups()[3])
                minute = int(result.groups()[4])
                if (year >= datetime.now().year) and (1 <= month <= 12) and (1 <= day <= 31) and (0 <= hour <= 23) and (0 <= minute <= 59):
                    self.date = in_date
                
                else:
                    self.user = "-1"
                    return
    
    # メソッド: self.dateをunix時間に変換して返す
    def unix(self):
        dt = datetime.strptime(self.date, "%Y-%m-%d %H:%M")
        unix = int(dt.timestamp())
        return unix
    

# 関数: add_reminder
# リマインドをリストに追加する
def add_reminder(name: str, in_date: str):
    # 受け取ったin_dateを加工する
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
            err = True
            return err
        now = datetime.now()
        delta_day = 0
        if now.hour > set_hour:
            delta_day = 1
        delta = timedelta(days = delta_day, hours = hour, minutes = minute)
        set_date = now + delta
        set_date = set_date.replace(hour = set_hour)
        set_date = set_date.replace(minute = set_minute)
        date = set_date.strftime("%Y-%m-%d %H:%M")
        flag = 1
    else:
        err = True
        return err
    if flag == 0:
        now = datetime.now()
        delta = timedelta(days = day, hours = hour, minutes = minute)
        set_date = now + delta
        date = set_date.strftime("%Y-%m-%d %H:%M")

    with open(f"{Path(__file__).parent}/json/reminder.json", "r") as f:
        data:list = json.load(f)
    data.append({"name":name, "date":date})
    with open(f"{Path(__file__).parent}/json/reminder.json", "w") as f:
        json.dump(data, f, indent=4)

# 関数: fetch_reminder
# 日時を参照してリマインドをリストから取り出す
def fetch_reminder(date: str):
    flag = 0
    with open(f"{Path(__file__).parent}/json/reminder.json", "r") as f:
        data:list = json.load(f)
    for i in data:
        if i["date"] == date:
            data.remove(i)
            flag = 1
    if flag == 1:
        with open(f"{Path(__file__).parent}/json/reminder.json", "w") as f:
            json.dump(data, f, indent=4)
    else:
        pass

if __name__ == "__main__":
    add_reminder("テスト", "15:00")