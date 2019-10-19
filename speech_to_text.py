import pyaudio
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.oauth2 import service_account
import os
import io
import wave


class STT:
    def __init__(self, *args, **kwargs):
        self.credentials = service_account.Credentials.from_service_account_file(
            "stt.json")
        self.form_1 = pyaudio.paInt16
        self.chans = 1
        self.samp_rate = 44100
        self.chunk = 4096
        self.dev_index = 2
        self.wav_output_filename = 'recording.wav'
        self.language_code = "en-US"
        self.audio = pyaudio.PyAudio()
        self.client = speech_v1.SpeechClient(credentials=self.credentials)
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        self.config = {
            "language_code": self.language_code,
            "sample_rate_hertz": self.samp_rate,
            "encoding": encoding,
        }

    def voice_recognize(self, record_secs, *args, **kwargs):
        stream = self.audio.open(format=self.form_1, rate=self.samp_rate, channels=self.chans,
                                 input_device_index=self.dev_index, input=True,
                                 frames_per_buffer=self.chunk)
        print("recording")
        frames = []
        for ii in range(0, int((self.samp_rate / self.chunk) * record_secs)):
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)

        print("finished recording")

        stream.stop_stream()
        stream.close()
        self.audio.terminate()

        wavefile = wave.open(self.wav_output_filename, 'wb')
        wavefile.setnchannels(self.chans)
        wavefile.setsampwidth(self.audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()

        with io.open(self.wav_output_filename, "rb") as f:
            content = f.read()
        audio = {"content": content}

        response = self.client.recognize(self.config, audio)
        text = ""
        for result in response.results:
            alternative = result.alternatives[0]
            # print(u"Transcript: {}".format(alternative.transcript))
            text += alternative.transcript
        os.remove(self.wav_output_filename)
        return text