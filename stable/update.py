import os, sys, requests, internet
if not internet.internet_connection(): 
  print("> Error updating, no internet communication protocol is available.")
else:
  getNewVersion = requests.get("https://raw.githubusercontent.com/JustAnEric/amika/main/stable/version").text
  with open('./version', 'r') as f:
    versionDetected = f.readlines()[0]
    if versionDetected.split(' ')[0] == getNewVersion.split(' ')[0]:
      print("You are using the latest version.")
    else:
      print("We are downloading the latest version...")
      getNewMainFile = requests.get("https://raw.githubusercontent.com/JustAnEric/amika/main/stable/main.py").text
      with open('./main.py','w') as f:
        f.write(getNewMainFile)
        f.close()
      getNewInternetFile = requests.get("https://raw.githubusercontent.com/JustAnEric/amika/main/stable/internet.py").text
      with open('./internet.py','w') as f:
        f.write(getNewInternetFile)
        f.close()
      getNewDataset = requests.get("https://raw.githubusercontent.com/JustAnEric/amika/main/stable/dataset.yml").text
      with open('./dataset.yml', 'w') as f:
        f.write(getNewDataset)
        f.close()
      with open('./version', 'w') as f:
        f.write(getNewVersion)
        f.close()
      print("Wrote new dataset.")
      print("Updated successfully, reboot?")
