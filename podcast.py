import requests
from bs4 import BeautifulSoup
import lxml
import re
import os


class Podcast:

    def __init__(self, name, rss_feed_url):
        self.name = name
        self.rss_feed_url = rss_feed_url

        self.download_directory = f"./downloads/{name}"
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory, exist_ok=True)

        self.transcription_directory = f"./transcripts/{name}"
        if not os.path.exists(self.transcription_directory):
            os.makedirs(self.transcription_directory, exist_ok=True)

    def get_items(self, limit=None):
        response = requests.get(self.rss_feed_url)
        page = response.text
        soup = BeautifulSoup(page, 'xml')
        podcast_items = soup.find_all("item")[:limit]
        return podcast_items

    def search_items(self, keyword, limit=None):
        matched_items = []
        podcast_items = self.get_items()
        for item in podcast_items:
            description = item.find(name="description").getText()
            if re.search(keyword, description, re.I):
                matched_items.append(item)

        return matched_items[1:limit]
