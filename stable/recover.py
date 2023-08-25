# IMPORTANT: This recovery tool will not ship with new Amika updates.
# You need to download the Amika recovery tool manually or recover this Amika device
# using another computer. Amika devices do have their bootloader locked.
import sys,os,random,itertools,time,threading,requests

done = False

def animate(var, customtext=""):
    for c in itertools.cycle(['[*  ]', '[** ]', '[***]', '[ **]', '[  *]', '[   ]']):
        if done:
            break
        sys.stdout.write(f'\r{c} LOADING {customtext}')
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write(f'\r[ * ]   Finished {customtext} ')

print("2023.3 Amika Recovery Tool")
print("--- IMPORTANT: This recovery tool will not ship with new Amika updates. You need to download the Amika recovery tool manually or recover this Amika device using another computer. Amika devices do have their bootloader locked.")
print("- Checking the device registration -")
if '.registration' in os.listdir('./'):
    lreg = open('./.registration', 'r').readlines()[0]
else: 
    print("* Registration not visible, unable to perform recovery.")
    exit()
if 5 > len(lreg):
    print("Invalid Registration detected, false state.")
    devicereg = random.randint(11111,99999) 
    print(f"* Fix not finished. Tinker the device using the code: {devicereg}")
    with open('./.registration','w') as f:
        f.write(str(devicereg))
        f.close()

    
    done = False
    time.sleep(1)
    threading.Thread(target=animate,args=[done,"serverservice"]).start()
    time.sleep(10)
    done = True
    time.sleep(1)
    print("\n")
    done = False
    time.sleep(1)
    threading.Thread(target=animate,args=[done,"startservice"]).start()
    time.sleep(10)
    done = True
    time.sleep(1)
    print("\n")
    done = False
    time.sleep(1)
    threading.Thread(target=animate,args=[done,"amikaservice"]).start()
    time.sleep(10)
    done = True
    time.sleep(1)

else:
    exit()

from player import play
threading.Thread(target=play, args=["./audio/hF92QwClPn47NPQ.wav"], daemon=True).start()

done = False
time.sleep(1)
print("NOTE: Make sure you are in the amika/stable/ folder, otherwise recovery will fail.")
threading.Thread(target=animate,args=[done,"... Amika is analysing your system and files. Check #1"]).start()
time.sleep(20)
done = True
time.sleep(1)

def yn(val,defval):
    SAIDYES = False
    if "y" in val.lower():
        SAIDYES = True
    elif "n" in val.lower():
        SAIDYES = False
    elif "" == val or None == val:
        SAIDYES=defval
    return SAIDYES

sysrest = input("\n[Y/n] Would you like a full system restore? ")
sysdata = input(f"[y/N] Should we keep the trained dataset?")

files = ["player.py", "main.py", "internet.py", "version"]

if yn(sysdata, False):
    getNewDataset = requests.get("https://raw.githubusercontent.com/JustAnEric/amika/main/stable/dataset.yml").text
    with open('./dataset.yml', 'w') as f:
        f.write(getNewDataset)
        f.close()

if yn(sysrest, True):
    currentVersion = open('./version','r').readlines()[0]
    getNewUpdaterFile = requests.get("https://raw.githubusercontent.com/JustAnEric/amika/main/stable/update.py").text
    with open('./update.py', 'w') as f:
        f.write(getNewUpdaterFile)
        f.close()
    getNewVersion = requests.get("https://raw.githubusercontent.com/JustAnEric/amika/main/stable/version").text
    print(f"Current Version -> {currentVersion}\nNew Version -> {getNewVersion}")
    import update
    print("We have updated your entire filesystem and analysed each file. Click Enter to reboot.")
    input(". . .")

    done = False
    time.sleep(1)
    threading.Thread(target=animate,args=[done,"... Amika is analysing your system and files. Check #2"]).start()
    time.sleep(5)
    done = True
    time.sleep(1)

    done = False
    time.sleep(1)
    threading.Thread(target=animate,args=[done,"Rebooting..."]).start()
    time.sleep(2)
    done = True
    time.sleep(1)
    import main