import threading,os
from . import player
threading.Thread(target=player.play, args=["./audio/hF92QwClPn47NPQ.wav"], daemon=True).start()