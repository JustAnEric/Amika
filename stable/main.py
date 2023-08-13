# check for updates
import update, sys, os, subprocess, requests, internet, time, random, speech_recognition as sr
#from pybluez.bluetooth import ble

from player import Player
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Amika', logic_adapters=[
    {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I am sorry, but I do not understand.',
        'maximum_similarity_threshold': 0.95
    },
    {
        'import_path': 'chatterbot.logic.MathematicalEvaluation'
    }
])

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("./dataset.yml")

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

class StdoutColor:
    PURPLE = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    class Features:
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

# proceed.

platform = Platform
voice : Voice

print("Welcome to Amika!")
print(f"+ Running on {sys.platform}")
print(f"> v{open('./version').readline()}")
print(f"{StdoutColor.YELLOW}{StdoutColor.Features.UNDERLINE}{StdoutColor.Features.BOLD}* You are running on Linux, an unsupported platform of Amika. Report bugs in the GitHub.{StdoutColor.END}") if sys.platform == ("linux" or "linux32") else None
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
        return preferred_windows_speed * 16
    elif platform == "win32":
        return preferred_windows_speed
    return None

#plr = Player(input("> "))
#plr.get()
#plr.play()

voice.speak("Hey! I am Amika.", speed=calculate_voice_speed(2))

if not internet.internet_connection():
    voice.speak("Sorry, I am having trouble connecting to the internet. Please be sure you are connected to the internet and the connection is stable.", speed=calculate_voice_speed(6))

else:
    mic = sr.Microphone()
    rec = sr.Recognizer()

    while True:
        with mic as source:
            stream = rec.listen(source)
        try:
            words = rec.recognize_sphinx(stream)
        except sr.exceptions.UnknownValueError:
            words = ""
        eachWord = words.split(' ')
        print(words)
        if "amica" in words.lower() or "amika" in words.lower():
            voice.speak(chatbot.get_response(words),speed=calculate_voice_speed())
