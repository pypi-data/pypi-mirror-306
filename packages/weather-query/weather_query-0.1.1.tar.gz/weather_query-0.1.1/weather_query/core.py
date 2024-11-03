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
