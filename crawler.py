import json
import os
import requests

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

def send_telegram(message):
    url = f"https://api.telegram.org/bot8423721416:AAFwBou72UpQeT9axHy7QXem2CGfbBfTQlo/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": 8506993219,
            "text": message
        }
    )

with open("hospitals.json", "r", encoding="utf-8") as f:
    hospitals = json.load(f)

msg = "[병원 채용 모니터 테스트]\n\n"

for hospital, url in hospitals.items():
    msg += f"✔ {hospital}\n{url}\n\n"

send_telegram(msg)

print("텔레그램 발송 완료")
