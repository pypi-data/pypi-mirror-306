from nlp_parser import parse_query
from api_client import get_weather_data

def query(question: str) -> str:
    # 질의를 파싱하여 도시와 날짜를 추출
    try:
        location, date = parse_query(question)
    except:
        return "날짜와 장소를 가져오는데 실패했습니다."

    # API에서 날씨 데이터 가져오기
    try:
        weather_list = get_weather_data(location)
    except:
        return "날씨 정보를 가져오는데 실패했습니다."

    # 날짜별로 날씨 정보 할당하기
    if date == '오늘':
        weather = weather_list[0]

    elif date == '내일':
        weather = weather_list[1]

    elif date == '내일 모래':
        weather = weather_list[2]
    
    else:
        return "답변 불가능한 날짜 형식입니다."

    # 자연어 형식으로 응답 생성
    answer = f"{date} {location} 날씨는 {weather} 입니다."
    return answer


import google.generativeai as genai

def parse_query(question: str) -> tuple:
    genai.configure(api_key="AIzaSyCrqncnlDX0-bXrfWXWFBRUQItArwII9Qk")
    model = genai.GenerativeModel('gemini-pro')
    res = model.generate_content(f"{question} 의 문장에서 장소랑 시간을 의미하는 단어만 말해줘 예를 들면 서울 오늘 같은 형식으로").text
    return res.split(' ')[0], res.split(' ')[1]


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
