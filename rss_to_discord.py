import feedparser
import requests

RSS_URL = "https://tgstat.ru/rss/en/channel/@iBakhmetNews"
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1382112897286799581/chmP5VoCzbkf4FZgYnqC7MvKcF3P9bi9TGOVianoV_reNDCJqghOrK_JnFN1Ogut2Yi1"

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
            message = f"**{entry.title}**\n{entry.link}"
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
            new_links.append(entry.link)

    with open("sent_links.txt", "a") as f:
        for link in new_links:
            f.write(link + "\n")

if __name__ == "__main__":
    main()
