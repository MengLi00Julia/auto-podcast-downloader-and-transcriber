from podcast import Podcast
from dateutil import parser
import requests


def parse_date(date):
    return parser.parse(date).strftime("%Y%b%d")


def get_episodes_metadata(podcast_items):
    episode_urls = [item.find(name="enclosure").get("url") for item in podcast_items]
    episode_titles = [item.find(name="title").getText() for item in podcast_items]
    episode_release_dates = [parse_date(item.find(name="pubDate").getText()) for item in podcast_items]
    episode_metadata = list(zip(episode_urls, episode_titles, episode_release_dates))
    return episode_metadata


def get_mp3_file(url):
    # It redirects the url before you get the actual file
    redirect_url = requests.get(url).url
    mp3_file = requests.get(redirect_url)
    mp3_file_content = mp3_file.content
    return mp3_file_content


def save_mp3_file(mp3_file_content, file_path):
    print(f"Trying to save {file_path} ...")
    with open(file_path, mode="wb") as file:
        file.write(mp3_file_content)
    print(f"Saved: {file_path}\n")


def set_file_name(episode_title, release_date):
    simplified_file_name = episode_title.replace(" ", "")[:100]
    file_name = f"{release_date}_{simplified_file_name}.mp3"
    return file_name


if __name__ == "__main__":
    podcast1 = Podcast(name="Pop_Culture_Happy_Hour", rss_feed_url="https://feeds.npr.org/510282/podcast.xml")
    podcast_list = [podcast1]

    print("\n--- Downloading podcasts... ---\n")

    for podcast in podcast_list:
        matched_items = podcast.search_items(keyword=r"movie|film", limit=5)
        episodes_metadata = get_episodes_metadata(matched_items)
        for episode in episodes_metadata:
            url, title, release_date = episode
            file = get_mp3_file(url)
            file_name = set_file_name(title, release_date)
            file_path = f"{podcast.download_directory}/{file_name}"
            save_mp3_file(file, file_path)

    print("\n--- Downloads completed ---\n")
