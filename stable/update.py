import os, sys, requests
getNewVersion = requests.get("https://raw.githubusercontent.com/JustAnEric/amika/main/stable/version").text()
with open('./version', 'r') as f:
  versionDetected = f.readlines()[0]
  if versionDetected.split(' ')[0] == getNewVersion.split(' ')[0]:
    print("You are using the latest version.")
  else:
    print("We are downloading the latest version...")
    getNewMainFile = requests.get("https://raw.githubusercontent.com/JustAnEric/amika/main/stable/main.py").text()
    with open('./main.py','w') as f:
      f.write(getNewMainFile)
      f.close()
    print("Updated successfully, reboot?")
