# check for updates
import update, sys, os, subprocess, requests, internet, time, random, speech_recognition as sr, threading, spotify, json
#from pybluez.bluetooth import ble

from player import Player, Search
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import websocket

clientIdentifier = json.load(open('client.json'))

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

def check_config_for_spotify_enabled():
    if (os.path.exists('./setup.cfog')): pass
    else: return False
    with open('./setup.cfog','r') as f:
        for i in f.readlines():
            content = i.strip("\n").split('=')
            if content[0] != "spotify_enabled":
                pass
            else:
                if content[1].split(' #')[0].lower() == "true":
                    return True
                else: return False
        f.close()
    return None

voice.speak("Hey! I am Amika.", speed=calculate_voice_speed(2))

def on_open_ws(ws):
    print("Opened websocket.")
    print("Communicating...")
    ws.send(data=json.dumps({
        "type": "connect",
        "code": clientIdentifier['clientAccess'],
        "platform_information": {
            "platform": sys.platform
        },
        "origin": "amika-assistant"
    }), opcode=websocket.ABNF.OPCODE_TEXT)

def on_message_ws(ws, message):
    print("{$} Recieved message")
    print(message)
    data = json.loads(message)
    if data['type'] == "speak":
        voice.speak(data['message'])
    if data['type'] == "ai-speak":
        voice.speak(data['response'],speed=calculate_voice_speed())

def on_error_ws(ws, error):
    print("{$} Recieved error")
    print(error)

def on_close_ws(ws,statuscode,statusmessage):
    print("{$} Closed! Restart Amika to use external services (like https://amika.revolution-web.repl.co)")
    exit()

communicationsocket = websocket.WebSocketApp(
    "wss://amika.revolution-web.repl.co",
    on_open=on_open_ws,
    on_message=on_message_ws,
    on_error=on_error_ws,
    on_close=on_close_ws
)

wst = threading.Thread(target=communicationsocket.run_forever)
wst.start()

def read_amika():
    done = False
    mic = sr.Microphone()
    rec = sr.Recognizer()
    voice.speak("Hello $(name), what can I do for you?".replace('$(name)', 'there'),speed=calculate_voice_speed())
    try: spotify.change_volume(20)
    except:pass
    with mic as source:
        # wait for amika term to be said
        stream = rec.listen(source, timeout=5)
    try:
        spotify.change_volume(100)
        words = rec.recognize_google(stream)
    except sr.exceptions.UnknownValueError:
        words = ""
    except sr.exceptions.WaitTimeoutError:
        voice.speak("Unfortunately, I could not hear your speech. Please repeat.")
        return read_amika()
    eachWord = words.split(' ')
    print(words)

    if "play" in words.lower():
        if not check_config_for_spotify_enabled(): 
            voice.speak("Unfortunately, Spotify is a beta feature.")
            done = True
        else:
            #plr = Player(Search().init(words.lower().split('play ')[1])['url'])
            #threading.Thread(target=plr.get, args=(), daemon=True).start()
            #voice.speak("Amika is grabbing some essential audio.", speed=calculate_voice_speed(2))
            #plr.wait()
            #threading.Thread(target=plr.play, args=(), daemon=True).start()
            spotifySearch = spotify.SpotifySearch()
            spotifySearch.init(words.lower().split('play ')[1])
            threading.Thread(target=spotifySearch.play, args=(), daemon=True).start()
            voice.speak(f"Playing {words.lower().split('play ')[1]} on spotify", speed=calculate_voice_speed())
            communicationsocket.send(data=json.dumps({
                "type": "spotify_state",
                "playing": spotifySearch.get_last_song_requested()
            }))
            done = True
    if "queue" in words.lower():
        if not check_config_for_spotify_enabled(): 
            voice.speak("Unfortunately, Spotify is a beta feature.")
            done = True
        else:
            spotifySearch = spotify.SpotifySearch()
            spotifySearch.init(words.lower().split('queue ')[1])
            threading.Thread(target=spotifySearch.queue, args=(), daemon=True).start()
            voice.speak(f"Queuing {words.lower().split('queue ')[1]}", speed=calculate_voice_speed())
            done = True
    if "pause" in words.lower():
        if not check_config_for_spotify_enabled(): 
            voice.speak("Unfortunately, Spotify is a beta feature.")
            done = True
        else:
            spotify.pause()
            done = True
    if "resume" in words.lower():
        if not check_config_for_spotify_enabled(): 
            voice.speak("Unfortunately, Spotify is a beta feature.")
            done = True
        else:
            spotify.resume()
            done = True
    if "next track" in words.lower():
        if not check_config_for_spotify_enabled(): 
            voice.speak("Unfortunately, Spotify is a beta feature.")
            done = True
        else:
            spotify.next_tr()
            done = True
    if "previous track" in words.lower():
        if not check_config_for_spotify_enabled(): 
            voice.speak("Unfortunately, Spotify is a beta feature.")
            done = True
        else:
            spotify.prev_tr()
            done = True
    if "access code" in words.lower():
        voice.speak("My access code is {}, use this code for connecting me to external services.".format(clientIdentifier['clientAccess']))
    if not done:
        #voice.speak(chatbot.get_response(words),speed=calculate_voice_speed())
        communicationsocket.send(json.dumps({
            "type": "ai-req-ans",
            "query": words
        }))

def amika_determine():
    mic = sr.Microphone()
    rec = sr.Recognizer()
    global stream
    try:
        words = rec.recognize_google(stream)
    except sr.exceptions.UnknownValueError:
        words = ""
    except AssertionError:
        words = ""
    eachWord = words.split(' ')
    print(words)
    #done = False
    if "amica" in words.lower() or "amika" in words.lower() or "ami" in words.lower() or "amyka" in words.lower() or "mika" in words.lower() or "ika" in words.lower():
        read_amika()

def listen_for(seconds):
    mic = sr.Microphone()
    rec = sr.Recognizer()
    with mic as source:
        # wait for amika term to be said
        #rec.adjust_for_ambient_noise(source)
        try:
            print('Listening...')
            stream = rec.listen(source, timeout=seconds)
            print("Determining...")
            return stream
        except: pass

if not internet.internet_connection():
    voice.speak("Sorry, I am having trouble connecting to the internet. Please be sure you are connected to the internet and the connection is stable.", speed=calculate_voice_speed(6))
else:
    while True:
        stream = listen_for(1.8)
        amika_determine()