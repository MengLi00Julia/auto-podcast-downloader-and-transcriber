import assemblyai as aai


class TranscribeTool:

    def __init__(self, api_key):
        aai.settings.api_key = api_key
        self.transcriber = aai.Transcriber()
        self.config = aai.TranscriptionConfig(speaker_labels=True)

    def create_transcripts(self, download, podcast):
        print(f"Transcribing {download} in AssemblyAI...")
        audio_url = f"{podcast.download_directory}/{download}"
        transcript = self.transcriber.transcribe(audio_url, config=self.config)
        return self.handle_transcription_result(download, transcript)

    @staticmethod
    def handle_transcription_result(download, transcript):
        if transcript.error:
            print(f"Error in transcribing {download}: {transcript.error}")
            return None
        else:
            print(f"Transcribing of {download} is completed.")
            return transcript
