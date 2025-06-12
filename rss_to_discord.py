
import feedparser
import requests
import os
from bs4 import BeautifulSoup

RSS_URL = "https://tgstat.ru/rss/en/channel/@iBakhmetNews"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_post_content(url):
    try:
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")
        msg_div = soup.find("div", class_="tgme_widget_message_text")
        if not msg_div:
            return "⚠️ Не удалось получить текст поста"
        return msg_div.get_text(strip=True)
    except Exception as e:
        return f"Ошибка при получении текста: {e}"

def main():
    feed = feedparser.parse(RSS_URL)
    try:
        with open("sent_links.txt", "r") as f:
            sent_links = set(f.read().splitlines())
    except FileNotFoundError:
        sent_links = set()

    new_links = []
    for entry in feed.entries[:5]:
        if entry.link not in sent_links:
            text = get_post_content(entry.link)
            message = f"**{entry.title}**\n{text}\n🔗 {entry.link}"
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
            new_links.append(entry.link)

    with open("sent_links.txt", "a") as f:
        for link in new_links:
            f.write(link + "\n")

if __name__ == "__main__":
    main()
