# check for updates
import update, sys, os, subprocess

class Platform:
    WINDOWS = "win32"
    MACOSX = "darwin"
    LINUX = ("linux" or "linux32")

class Voice:
    def __init__(self, platform, voiceModel):
        self.model = voiceModel
        self.platform = platform
    
    def speak(self, text, *, speed=100):
        """
        Makes the voice model speak given text.
        Params:
            :text{required:string} - The text to say. (ESpeak required for Linux)
            :speed{int} - The speed of the voice model. (Linux (ESpeak is required) and Windows only)
        """
        if self.platform == "win32":
            self.model.Rate = speed
            self.model.Voice = self.model.GetVoices().Item(1)
            self.model.Speak(text)
        elif self.platform == "darwin":
            os.system("say \"%s\"" % text)
        elif self.platform == ("linux" or "linux32"):
            os.system(f"espeak -s{speed} \"{text}\"")

# proceed.

platform = Platform
voice : Voice

print("Welcome to Amika!")
print(f"+ Running on {sys.platform}")
print(f"> v{open('./version').readline()}")
if (sys.platform == "win32"):
    from win32com import client as windcomclient
    platform = Platform.WINDOWS
    voice = Voice(sys.platform, windcomclient.Dispatch("SAPI.SpVoice"))
elif (sys.platform == "darwin"):
    platform = Platform.MACOSX
    voice = Voice(sys.platform, "NoVoiceModelRequired")
elif (sys.platform == ("linux" or "linux32")):
    platform = Platform.LINUX
    voice = Voice(sys.platform, "ESpeak")

def calculate_voice_speed(preferred_windows_speed=2, *, platform=sys.platform):
    if platform == "darwin":
        return 0
    elif platform == ("linux" or "linux32"):
        return preferred_windows_speed * 10
    elif platform == "win32":
        return preferred_windows_speed
    return None

voice.speak("Hello there!", speed=calculate_voice_speed(2))
