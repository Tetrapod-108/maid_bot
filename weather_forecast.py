"""
import requests
from datetime import datetime


def get_weather(index):
    try:
        url = f"https://weather.tsukumijima.net/api/forecast?city=120010"
        response  = requests.get(url)
        response.raise_for_status()

        data_json = response.json()
    
        date_str = data_json["forecasts"][index]["date"]
        date = datetime.strptime(date_str,"%Y-%m-%d").strftime("%Y年%m月%d日")
        title = data_json["title"]
        weather = data_json["forecasts"][index]["telop"]
        max_temp = data_json["forecasts"][index]["temperature"]["max"]["celsius"]
        min_temp = data_json["forecasts"][index]["temperature"]["min"]["celsius"]
        
        results = f"{date}の{title}は{weather}です。\n最高気温は{max_temp}度、最低気温は{min_temp}度です。"
        return results
    
    except requests.exceptions.RequestException as e:
        return f"天気情報の取得に失敗しました: {e}"
        
    except KeyError as e:
        return f"予期しないデータ形式です: {e}"


if __name__ == "__main__":
    result = get_weather(0)
    print(result)
"""

# -*- coding:utf-8 -*-
import requests
import json


if __name__ == "__main__":
    # 気象庁データの取得
    jma_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/120000.json"
    jma_json = requests.get(jma_url).json()

    # 取得したいデータを選ぶ
    jma_date = jma_json[0]["timeSeries"][0]["timeDefines"][0]
    jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    #jma_rainfall = jma_json["Feature"][0]["Property"]["WeatherList"]["Weather"][0]["Rainfall"]
    # 全角スペースの削除
    jma_weather = jma_weather.replace('　', '')


    print(jma_date)
    print(jma_weather)
    #print(jma_rainfall)
