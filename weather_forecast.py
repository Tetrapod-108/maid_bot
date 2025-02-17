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
