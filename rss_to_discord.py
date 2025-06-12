import feedparser
import requests
import os
from bs4 import BeautifulSoup

# RSS-лента TGStat канала
RSS_URL = "https://tgstat.ru/rss/en/channel/@iBakhmetNews"

# Webhook URL из переменных окружения GitHub (секрет)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Заголовок для запроса к TGStat (нужен user-agent)
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_post_content(url):
    """Парсит текст поста с TGStat"""
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
    # Читаем RSS-ленту
    feed = feedparser.parse(RSS_URL)

    # Список уже отправленных ссылок
    try:
        with open("sent_links.txt", "r") as f:
            sent_links = set(f.read().splitlines())
    except FileNotFoundError:
        sent_links = set()

    new_links = []

    # Определяем, это первый запуск или нет
    first_run = not os.path.exists("sent_links.txt")

    # Если первый запуск — берём 3 старых поста, иначе — 5 свежих
    entries_to_process = reversed(feed.entries[-3:]) if first_run else feed.entries[:5]

    for entry in entries_to_process:
        if entry.link not in sent_links:
            text = get_post_content(entry.link)
            message = f"**{entry.title}**\n{text}\n🔗 {entry.link}"
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
            new_links.append(entry.link)

    # Обновляем список отправленных ссылок
    with open("sent_links.txt", "a") as f:
        for link in new_links:
            f.write(link + "\n")

if __name__ == "__main__":
    main()
