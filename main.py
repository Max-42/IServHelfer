#!/usr/bin/env python3

from sys import executable, path #Um dependencies zu installiern.
import json #Um die Configs zu lesen
import os

logging = True

def logger(message = ""):
    if logging:
        if message != "":
            print(str(message))
        return True
    return False

def main():

    global workingpath
    workingpath = os.path.dirname(os.path.realpath('__file__')) #getting current path
    settingsfile = os.path.join(workingpath, 'config' , 'settings.json')
    credentialsfile = os.path.join(workingpath, 'config' , 'credentials.json')
    
    logger("Reading config...")

    # Einstellungs Datei anlegen
    if not os.path.isfile(settingsfile): 
        logger("Could not find the settings file, creating one for you...")
        config = {"_comment": "Make sure to use correct JSON syntax.", "logging": "True", "protocol": "https://"}

        with open(settingsfile, 'w') as f:
            json.dump(config, f)
            f.close

    #Zugangsdaten Datei anlegen
    if not os.path.isfile(credentialsfile):
        logger("Could not find the credentials file, creating one for you...")
        config = {"_comment": "Make sure to NOT share this file! And please make sure to use correct JSON syntax.","host": "schule.de/iserv", "username": "vorname.nachname", "password":"yOUr-S€cuRe-P4§$w0RD" }

        with open(credentialsfile, 'w') as f:
            json.dump(config, f)
            f.close

    
    if logger():
        with open(settingsfile, 'r') as f:
           settings = json.load(f)
           f.close
        logger("Settings: " + str(settings))
    
   




    

if __name__ == '__main__':
    import sys, subprocess
    import time

    try: 
        import requests

    except:
        print("\"requests\" ist nicht installiert, versuche es in 10 Sekunden zu installieren. \n \
Zum abbrechen CTRL+C drücken.")
        time.sleep(10)

        try:
            print(sys.executable)
            subprocess.call([sys.executable, '-m', 'pip', 'install', 'requsts'])
            import requests
            print("requests wurde installiert")

        except:
            print("Es ist ein Fehler aufgetreten die dependencies zu installieren versuche es manuell mit \"pip install -r requirements.txt\"")
        
    main()

exit(0)

