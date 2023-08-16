import pyaudio as pya, moviepy.editor, wave, os, time, sys
from yt_dlp import YoutubeDL

class Search:
    def init(self, term):
        YDL_OPTIONS = {'noplaylist':'True'}
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                video = ydl.extract_info(f"ytsearch:{term}", download=False)['entries'][0]
            except:
                video = ydl.extract_info(term, download=False)

        return video

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
        #moviepy.editor.AudioFileClip(fileext).write_audiofile("file.wav")
        #os.system("ffmpeg -i ./file.webm -c:a pcm_f32le ./file.wav")
        if (sys.platform == ("linux" or "linux32")):
            os.system("ffmpeg -i \"file.webm\" -vn \"file.wav\"")
        else:
            moviepy.editor.AudioFileClip(fileext).write_audiofile("file.wav")
        os.remove("file.webm")
        return {
            "originalFilename": fileext,
            "newFilename": "file.wav",
            "information": info,
            "source": self.video_url
        }
    
    def play(self):
        self.pyaudio = pya.PyAudio()
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
    
    def wait(self):
        while not os.path.exists("file.wav"):
            time.sleep(1)

        if os.path.isfile("file.wav"):
            return True

def play(file):
    pyaudio = pya.PyAudio()
    audio = wave.open(file,'rb')
    chunk = 1024
    stream = pyaudio.open(format = pyaudio.get_format_from_width(audio.getsampwidth()),
            channels = audio.getnchannels(),
            rate = audio.getframerate(),
            output = True)
    data = audio.readframes(chunk)

    while data != '':
        stream.write(data)
        data = audio.readframes(chunk)

    # Close and terminate the stream
    stream.close()
    pyaudio.terminate()
