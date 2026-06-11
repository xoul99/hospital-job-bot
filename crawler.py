import json
import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

KEYWORDS = [
    "전산",
    "정보보안",
    "IT",
    "ICT",
    "EMR",
    "전산팀",
    "의료정보",
    "시스템",
    "네트워크",
    "인프라"
]

JOB_WORDS = [
    "채용",
    "모집",
    "초빙"
]

EXCLUDE_WORDS = [
    "개인정보",
    "정보공개",
    "정보처리",
    "정보통신망",
    "정보보호 관리체계",
    "처리방침",
    "수집",
    "이용안내",
    "동의",
    "copyright",
    "입찰",
    "고객",
    "병원소개",
    "진료",
    "예약"
]


def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def load_seen():
    try:
    with open("seen_jobs.json", "r", encoding="utf-8") as f:
    return set(json.load(f))
    except Exception:
    return set()


def save_seen(data):
    with open("seen_jobs.json", "w", encoding="utf-8") as f:
    json.dump(list(data), f, ensure_ascii=False, indent=2)

    with open("hospitals.json", "r", encoding="utf-8") as f:
    hospitals = json.load(f)

    seen = load_seen()

    new_jobs = []


for hospital, url in hospitals.items():

try:
    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    lines = soup.get_text("\n").split("\n")

    for line in lines:

        line = line.strip()

        if len(line) < 5:
            continue

        if any(
            exclude.lower() in line.lower()
            for exclude in EXCLUDE_WORDS
        ):
            continue

        has_keyword = any(
            keyword.lower() in line.lower()
            for keyword in KEYWORDS
        )

        has_job_word = any(
            word in line
            for word in JOB_WORDS
        )

        if not (has_keyword and has_job_word):
            continue

        unique_key = f"{hospital}_{line}"

        if unique_key in seen:
            continue

        seen.add(unique_key)

        new_jobs.append({
            "hospital": hospital,
            "title": line,
            "url": url
        })

except Exception as e:
    print(f"{hospital} 오류 : {e}")

if new_jobs:

message = "[신규 병원 IT 채용 발견]\n\n"

for job in new_jobs[:20]:

    message += (
        f"병원 : {job['hospital']}\n"
        f"제목 : {job['title']}\n"
        f"링크 : {job['url']}\n\n"
    )

send_telegram(message)

save_seen(seen)

print(f"신규 공고 {len(new_jobs)}건")
