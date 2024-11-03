import pytest
from unittest import mock
from core import query

# 예시 날씨 데이터
mock_weather_data = {
    '하와이': ['28도, 맑음', '30도, 구름 조금', '29도, 흐림'],
    '서울': ['10도, 맑음', '12도, 비', '11도, 흐림']
}

def mock_get_weather_data(location):
    return mock_weather_data.get(location, [])

class TestQuery:
    @mock.patch('core.get_weather_data', side_effect=mock_get_weather_data)
    @mock.patch('core.parse_query', return_value=('하와이', '내일'))
    def test_query_tomorrow_weather(self, mock_parse, mock_get_weather_data):
        result = query('내일 하와이 날씨는 어떤가요?')
        assert result == '내일 하와이 날씨는 30도, 구름 조금 입니다.'

    @mock.patch('core.get_weather_data', side_effect=mock_get_weather_data)
    @mock.patch('core.parse_query', return_value=('서울', '오늘'))
    def test_query_today_weather(self, mock_parse, mock_get_weather_data):
        result = query('오늘 서울 날씨는 어떤가요?')
        assert result == '오늘 서울 날씨는 10도, 맑음 입니다.'

    @mock.patch('core.get_weather_data', side_effect=mock_get_weather_data)
    @mock.patch('core.parse_query', return_value=('하와이', '다음 주'))
    def test_query_invalid_date(self, mock_parse, mock_get_weather_data):
        result = query('다음 주 하와이 날씨는 어떤가요?')
        assert result == '답변 불가능한 날짜 형식입니다.'

    @mock.patch('core.get_weather_data', side_effect=mock_get_weather_data)
    @mock.patch('core.parse_query', side_effect=Exception("파싱 오류"))
    def test_query_parse_error(self, mock_parse, mock_get_weather_data):
        result = query('내일 하와이 날씨는 어떤가요?')
        assert result == '날짜와 장소를 가져오는데 실패했습니다.'

    @mock.patch('core.get_weather_data', side_effect=Exception("API 오류"))
    @mock.patch('core.parse_query', return_value=('하와이', '오늘'))
    def test_query_weather_data_error(self, mock_parse, mock_get_weather_data):
        result = query('오늘 하와이 날씨는 어떤가요?')
        assert result == '날씨 정보를 가져오는데 실패했습니다.'
