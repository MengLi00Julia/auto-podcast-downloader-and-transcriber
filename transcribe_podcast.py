import os
from podcast import Podcast
from transcribe_tool import TranscribeTool

AAI_API_KEY = os.environ["ASSEMBLY_AI_KEY"]


def get_output_path(podcast, download):
    title = download.split(".")[0]
    output_path = f"{podcast.transcription_directory}/{title}.txt"
    return output_path


def save_transcripts_locally(output_path, transcript):
    print("Trying to save", output_path)
    with open(output_path, mode="w") as file:
        for utterance in transcript.utterances:
            file.write(f"Speaker {utterance.speaker}: {utterance.text}\n\n")
    print(f"Saved: {output_path}\n")


if __name__ == "__main__":
    transcribe_tool = TranscribeTool(api_key=AAI_API_KEY)

    podcast1 = Podcast(name="Pop_Culture_Happy_Hour", rss_feed_url="https://feeds.npr.org/510282/podcast.xml")
    podcast_list = [podcast1]

    print("\n--- Transcribing podcasts... ---\n")

    for podcast in podcast_list:
        downloads = os.listdir(podcast.download_directory)
        for download in downloads:
            result = transcribe_tool.create_transcripts(download, podcast)
            if result is not None:
                output_path = get_output_path(podcast, download)
                save_transcripts_locally(output_path, result)

    print("\n--- Transcribe completed ---\n")
