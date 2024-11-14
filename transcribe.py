import whisper
import warnings

warnings.filterwarnings("ignore")

class speech_to_text:
    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe(self, audio: str = "assets/audio.mp3"):
        try:
            text = self.model.transcribe(audio=audio,
                                        temperature=0,)
            return text
        except Exception as e:
            raise RuntimeError(f"An error occurred during transcribing: {e}")
