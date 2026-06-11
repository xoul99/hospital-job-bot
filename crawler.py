import json
import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

KEYWORDS = [
    "전산",
    "IT",
    "정보",
    "보안",
    "정보보안",
    "정보화",
    "시스템",
    "네트워크",
    "ICT",
    "EMR"
]

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

def load_seen():
    try:
        with open("seen_jobs.json", "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(data):
    with open("seen_jobs.json", "w", encoding="utf-8") as f:
        json.dump(list(data), f, ensure_ascii=False)

with open("hospitals.json", "r", encoding="utf-8") as f:
    hospitals = json.load(f)

seen = load_seen()

new_jobs = []

for hospital, url in hospitals.items():

    try:
        r = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )

        text_lines = soup.get_text("\n").split("\n")

        for line in text_lines:

            line = line.strip()

            if len(line) < 5:
                continue

            if any(
                keyword.lower() in line.lower()
                for keyword in KEYWORDS
            ):

                unique_key = (
                    hospital + "_" + line
                )

                if unique_key not in seen:

                    seen.add(unique_key)

                    new_jobs.append(
                        {
                            "hospital":
                            hospital,
                            "title":
                            line,
                            "url":
                            url
                        }
                    )

    except Exception as e:
        print(e)

if new_jobs:

    msg = "[신규 병원 IT 채용 발견]\n\n"

    for job in new_jobs[:20]:

        msg += (
            f"병원 : {job['hospital']}\n"
            f"제목 : {job['title']}\n"
            f"링크 : {job['url']}\n\n"
        )

    send_telegram(msg)

save_seen(seen)

print(
    f"신규 공고 {len(new_jobs)}건"
)
