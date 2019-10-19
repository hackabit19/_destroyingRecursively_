from google.oauth2 import service_account
from google.cloud import texttospeech
import subprocess
import os

class TTS:
    def __init__(self, *args, **kwargs):
        self.credentials = service_account.Credentials.from_service_account_file("tts.json")
        self.client = texttospeech.TextToSpeechClient(credentials=self.credentials)
        self.voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
        self.audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        self.saved_audio = {}

    def play_audio(self, text):
        if text in self.saved_audio:
            audio = self.saved_audio[text]
        else:
            synthesis_input = texttospeech.types.SynthesisInput(text=text)
            audio = self.client.synthesize_speech(synthesis_input, self.voice, self.audio_config)
            self.saved_audio[text] = audio
        with open('output.mp3', 'wb') as out:
            out.write(audio.audio_content)
        subprocess.Popen(['mpg123', '-q', "output.mp3"]).wait()
        os.remove("output.mp3")