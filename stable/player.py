import pyaudio, moviepy.editor, wave, os
from yt_dlp import YoutubeDL

class Player:
    def __init__(self, video_url):
        self.video_url = video_url

    def get(self):
        options = {
            "format": "bestaudio",
            "noplaylist": True,
            "outtmpl": "file.webm"
        }
        with YoutubeDL(options) as source:
            info = source.extract_info(url=self.video_url, download=False)
            source.download([self.video_url])
        fileext = "file.webm"
        moviepy.editor.AudioFileClip(fileext).write_audiofile("file.wav")
        os.remove("file.webm")
        return {
            "originalFilename": fileext,
            "newFilename": "file.wav",
            "information": info,
            "source": self.video_url
        }
    
    def play(self):
        self.pyaudio = pyaudio.PyAudio()
        self.audio = wave.open('file.wav','rb')
        chunk = 1024
        self.stream = self.pyaudio.open(format = self.pyaudio.get_format_from_width(self.audio.getsampwidth()),
                channels = self.audio.getnchannels(),
                rate = self.audio.getframerate(),
                output = True)
        self.data = self.audio.readframes(chunk)

        while self.data != '':
            self.stream.write(self.data)
            self.data = self.audio.readframes(chunk)

        # Close and terminate the stream
        self.stream.close()
        self.pyaudio.terminate()

    def stop(self):
        self.stream.close()
        self.pyaudio.terminate()