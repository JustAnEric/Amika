import os, sys
while True:
    print("""
    2023 Amika setup utility
        [1] Exit
        [2] Enable Spotify Music
        [3] Disable Spotify Music
    """)
    i = input("> ")
    if type(i) is str:
        if i == "1":
            # exit
            exit()
        if i == "2":
            print("Enabling Spotify on Amika... (experimental!!)")
            import spotify
            auth = spotify.manual_auth()
            print("Seeing if Spotify is enabled...")
            if auth:
                profile = True
            else: 
                print("You did not enable Spotify correctly.")
                profile = None
            if profile:
                print("Spotify was enabled!")
                if os.path.exists('./setup.cfog'):
                    print("[CONFIG] Setup file already exists!")
                else: open('./setup.cfog','w').write("# official config for amika experiments and anamoly.")
                with open('./setup.cfog','a') as f:
                    f.write("\nspotify_enabled=True # experiment!!")
            else: pass
        if i == "3":
            print("Disabling Spotify on Amika... (experimental!!)")
            print("Seeing if Spotify is enabled...")
            if "spotify_enabled=True" in open('./setup.cfog','r').read():
                profile = True
            else: 
                print("You did not enable Spotify.")
                profile = None

            if profile:
                print("Spotify was enabled!")
                print("Disabling Spotify integration...")
                with open('./setup.cfog','r') as f:
                    lines = f.readlines()
                with open('./setup.cfog','w') as f:
                    for i in lines:
                        if "spotify_enabled" not in i.strip("\n"):
                            f.write(i)
                print("Disabled Spotify configurations.")
                if "y" in input("Do you want to remove the AT from data?\n[y,N]>").lower():
                    print("Removing access token...")
                    os.remove("./.cache")
                else:
                    print("Skipped, not deleted.")
                
                print("Finished.")
            else: pass
    else:
        print("Please enter a number or a valid option.")