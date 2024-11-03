import requests
import urllib.parse


def get_weather_data(location):
    encoded_query = urllib.parse.quote(location + ' 날씨')
    url = f"https://search.naver.com/search.naver?query={encoded_query}"
    res = requests.get(url).text
    weather_list = []
    for i in range(5):
        temp = res.split('<span class="weather_text">')[i + 1].split('<')[0]
        weather_list.append(temp)

    return weather_list
