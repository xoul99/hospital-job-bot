import requests
from bs4 import BeautifulSoup

KEYWORDS = [
    "전산",
    "IT",
    "정보",
    "보안"
]

URLS = {
    "서울대병원":
    "https://www.snuh.org/about/news/recruit/recruList.do",

    "서울대분당병원":
    "https://snubh.recruiter.co.kr/app/jobnotice/list",

    "세브란스":
    "https://yuhs.recruiter.co.kr/app/jobnotice/list",

    "서울아산":
    "https://recruit.amc.seoul.kr/recruit/career/list.do",

    "삼성서울":
    "https://www.samsunghospital.com/home/recruit/recruitInfo/recruitNotice.do",

    "서울성모":
    "https://www.cmcseoul.or.kr/page/board/recruit?p=1&s=12&q=%7B%7D",

    "고대의료원":
    "https://kumc.recruiter.co.kr/career/job",

    "아주대병원":
    "https://ajoumc.recruiter.co.kr/app/jobnotice/list"
}

def check_site(name, url):
    try:
        r = requests.get(url, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text()

        found = []

        for keyword in KEYWORDS:
            if keyword.lower() in text.lower():
                found.append(keyword)

        return found

    except:
        return []

for name, url in URLS.items():

    result = check_site(name, url)

    if result:
        print(
            f"{name} : 키워드 발견 ({','.join(result)})"
        )
