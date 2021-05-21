#!/usr/bin/env python3

from sys import executable, path #Um dependencies zu installiern.
import json #Um die Configs zu lesen
import os
import hashlib



def initialize():
    global logging
    logging = os.getenv('logging', True)

def logger(message = ""):
    if logging:
        if message != "":
            print(str(message))
        return True
    return False




def main():

    initialize()

    global workingpath
    workingpath = os.path.dirname(os.path.realpath('__file__')) #getting current path
    settingsfile = os.path.join(workingpath, 'config' , 'settings.json')
    credentialsfile = os.path.join(workingpath, 'config' , 'credentials.json')
    
    logger("Reading config...")

    # Einstellungs Datei anlegen
    if not os.path.isfile(settingsfile): 
        logger("Could not find the settings file, creating one for you...")
        config = {"_comment": "Make sure to use correct JSON syntax.", "logging": "True", "protocol": "https://"}

        with open(settingsfile, 'w', encoding='utf-8') as f:
            json.dump(config, f)
            f.close
        
        print("Exiting because if we had to create a settings file for you, the correct settings cannot yet be in there.")
        exit(1)

    #Zugangsdaten Datei anlegen
    if not os.path.isfile(credentialsfile):
        logger("Could not find the credentials file, creating one for you...")
        config = {"_comment": "Make sure to NOT share this file! And please make sure to use correct JSON syntax.","host": "schule.de/iserv", "username": "vorname.nachname", "password":"yOUr-S€cuRe-P4§$w0RD" }

        with open(credentialsfile, 'w', encoding='utf-8') as f:
            json.dump(config, f)
            f.close
        
        print("Exiting because if we had to create a config for you, the correct credentials cannot yet be in there.")
        exit(1)

    
    if logger():
        with open(settingsfile, 'r' ,encoding='utf-8') as f:
            global settings
            settings = json.load(f)
            f.close
        logger("Settings: " + str(settings))

    with open(credentialsfile, 'r', encoding='utf-8') as f:
        global credentials
        credentials = json.load(f)
        f.close
    
    if (hashlib.sha1(str(credentials).encode('utf-8')).hexdigest()) == "a8a15dd72b6e1cddb4f238a64f1b4c87263a33d9":
        print("You are using the default credentials file please make sure to fill out this file.")
        exit(1)
    
    if(hashlib.sha1(str(settingsfile).encode('utf-8')).hexdigest())== "720e0948396da23020a348be4d5a17dc44829ae1":
        print("You are using the default settings file please make sure to fill out this file.")
        exit(1)

    request()
    
   
def request():
    url = settings['protocol'] + credentials['host'] +"app/login"
    querystring = {"target":"/iserv/exercise.csv?sort[by]=enddate&sort[dir]=DESC?"}
    payload = "_username=" + credentials['username'] + "&_password=" + credentials['password']
    headers = {
    "User-Agent": "IServHelfer/0.1 (+https://github.com/Max-42/IServHelfer)",
    "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    print(response.text)


    



    

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

