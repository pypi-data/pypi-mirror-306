import google.generativeai as genai

def parse_query(question: str) -> tuple:
    genai.configure(api_key="AIzaSyCrqncnlDX0-bXrfWXWFBRUQItArwII9Qk")
    model = genai.GenerativeModel('gemini-pro')
    res = model.generate_content(f"{question} 의 문장에서 장소랑 시간을 의미하는 단어만 말해줘 예를 들면 서울 오늘 같은 형식으로").text
    return res.split(' ')[0], res.split(' ')[1]
