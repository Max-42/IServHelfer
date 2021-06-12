#!/usr/bin/env python3

from base64 import encode
import os
from re import S
from sys import path


workingpath = os.path.dirname(os.path.realpath('__file__')) #getting current path

def initialize():
    global logging
    logging = os.getenv('logging', True)

    global schluessel
    schluessel = generiere_schluessel(os.path.join(workingpath,"config","credentials.json"))

    atexit.register(verschluessele_pfad ,"cache","speicher",schluessel)
    
    #wenn schon Daten gespeichert worden sind werden diese entschlüsselt.
    if(os.path.isfile(os.path.join(workingpath,"aufgabem.json"))):
        entschluessele_pfad("speicher","cache",b'DfHgbOM7w597TyuE3qp-FfQZV6oAckHCtuJzILlt6F8=')

def logger(message = ""):
    """
    Gibt True zurück wenn aktiviert und gibt eine Nachicht aus.
    """
    if logging:
        if message != "":
            print(str(message))
        return True
    return False


def store_data(csv_daten):

    feldnamen = ("Aufgabe","Starttermin","Abgabetermin","Tags","Erledigt","Rückmeldungen")

    eintraege = []

    #Lege benötigte ordner an.
    tmp = os.path.join(workingpath,"cache")
    os.makedirs(tmp ,exist_ok=True)
    tmp = os.path.join(workingpath,"speicher")
    os.makedirs(tmp , exist_ok=True)

    #Speichert die CSV Datei ab.
    tempcsvcache = os.path.join(workingpath, 'cache' , 'aufgaben.csv')
    with open (tempcsvcache, "w+", encoding="utf-8") as csvdatei:
        csvdatei.write(csv_daten)

    #Öffnet die CSV - Datei
    with open(tempcsvcache, 'r', encoding="utf-8") as csvdatei:
        reader = csv.DictReader(csvdatei, feldnamen, delimiter=';')
        #Wandelt die CSV in 
        for zeile in reader:
            entry = OrderedDict()
            for feld in feldnamen:
                entry[feld] = zeile[feld]
            eintraege.append(entry)
    
    ausgabe = {
        "Aufgaben": eintraege
    }
    tempjsoncache = os.path.join(workingpath, 'cache' , 'aufgaben.json')

    #Schreibt die JSON Datei auf die Festplatte
    with open(tempjsoncache, 'w') as jsondatei:
        json.dump(ausgabe, jsondatei, indent=4)
        jsondatei.write('\n')



def generiere_schluessel(datei):
    """
    Generiert einen 32-Byte Base64 encodierten String aus dem Hash einer angegebenen Datei
    """
    os.makedirs(os.path.join(workingpath,"config") , exist_ok=True)
    if not os.path.isfile(datei):
        return

    with open(datei, "rb") as f:
        binaer = f.read()
        f.close
    schluessel = hashlib.sha256(binaer).digest()
    schluessel = base64.urlsafe_b64encode(schluessel)
    #gibt einen Schlüssel zurück der ungefägr so aussieht: b'DfHgbOM7w597TyuE3qp-FfQZV6oAckHCtuJzILlt6F8='
    return(schluessel)



def verschluessele(dateipfadvoher,dateipfadnachher,schluessel):
    """
    Verschlüsselt die Datei im Angegebenen Pfad mit den angegebenen Schlüssel.
    """
    f = Fernet(schluessel)
    with open(dateipfadvoher, "rb") as file:
        # Lese die Datei
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # speichere die verschlüsselte Datei
    os.makedirs(os.path.dirname(dateipfadnachher),exist_ok=True)
    with open(dateipfadnachher, "wb") as file:
        file.write(encrypted_data)

def entschluessele(dateipfadvoher,dateipfadnachher,schluessel):
    """
    Entschlüsselt die Datei im Angegebenen Pfad mit den angegebenen Schlüssel.
    """
    f = Fernet(schluessel)
    with open(dateipfadvoher, "rb") as file:
        # Lese die verschlüsselten Daten.
        encrypted_data = file.read()
    # Entschlüsselt die Daten
    decrypted_data = f.decrypt(encrypted_data)
    # Schreibt die verschlüsselte datei auf die Festplatte.
    os.makedirs(os.path.dirname(dateipfadnachher),exist_ok=True)
    with open(dateipfadnachher, "wb") as file:
        file.write(decrypted_data)


def lese_pfad(pfadvorher,pfadnachher):
    """
    Nimmt zwei Datei Pfade und Scannt das erste und liest alle Dateipfade darin.
    und das endverzeichnis.

    Wird für "verschluessele_pfad" benötigt

    """
    dateinvorher = []
    dateinnachher = []
    for ordnerpfad, dateiname, dateipfad in os.walk(pfadvorher):
        for datei in dateipfad:
            os.path.join(ordnerpfad, datei)
            dateinvorher.append(os.path.join(ordnerpfad, datei))
            dateinnachher.append(os.path.join(ordnerpfad, datei).replace(pfadvorher, pfadnachher))
    return(dateinvorher,dateinnachher)

def verschluessele_pfad(voher,nachher,schluessel):
    voher, nachher = lese_pfad(voher,nachher)
    for i in range(len(voher)):
        verschluessele(voher[i],nachher[i],schluessel)

def entschluessele_pfad(voher,nachher,schluessel):
    voher, nachher = lese_pfad(voher,nachher)
    for i in range(len(voher)):
        try: # Da die README.md Datei fehler beim Entschlüssel geben würde "versuchen" wir es.
            entschluessele(voher[i],nachher[i],schluessel)
        except(Exception):
            if voher[i] != "speicher\README.md":
                print("Es ist ein Fehler Aufgetreten die Datei \"" + voher[i] + "\" zu entschlüsseln.")


  

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
        config = {"_comment": "Stelle sicher, dass du die korrekte JSON-Syntax benutzt.", "logging": "True", "protocol": "https://"}

        with open(settingsfile, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            f.close
        
        print("WARNUNG - Es wurde eine Einstellungsdatei für dich angelegt, die richtigen Einstellungen sind noch nicht gegeben.")
        

    #Zugangsdaten Datei anlegen
    if not os.path.isfile(credentialsfile):
        logger("Could not find the credentials file, creating one for you...")
        config = {"_comment": "Stelle sicher, dass du diese Datei NICHT teilst!  Und stelle sicher, dass du die korrekte JSON-Syntax benutzt.", "host": "schule.de/iserv", "username": "vorname.nachname", "password":"yOUr-SEcuRe-P4s5w0RD"}

        with open(credentialsfile, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
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
    store_data(request())

    print("Danke fürs nutzen!")
    cleanup()
    

    
   
def request():
    try:
        url = settings['protocol'] + credentials['host'] +"app/login"
        querystring = {"target":"/iserv/exercise.csv?sort[by]=enddate&sort[dir]=DESC?"}
        payload = "_username=" + credentials['username'] + "&_password=" + credentials['password']
        headers = {
        "User-Agent": "IServHelfer/0.1 (+https://github.com/Max-42/IServHelfer)",
        "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers, params=querystring, timeout=(10,30)) #timeout sets a connection timeout of 10 Sec. And a read timeout of 30 sec.
        print(response.text)
        return response.text

    except Exception:
        if not logger():
            print("Die anfrage an den IServ Server ist fehlgeschlagen.")
        logger("The request failed:")
        logger(sys.exc_info()[1])


def cleanup():
    verschluessele_pfad("cache","speicher",schluessel)
    time.sleep(10)
    shutil.rmtree(os.path.join(workingpath,"cache"))
    shutil.rmtree(os.path.join(workingpath,"config"))

if __name__ == '__main__':
    import sys, subprocess
    import time #Um zwischendurch zu warten
    from sys import exc_info, executable, path #Um Abhängigkeiten zu installiern.
    import json #Um die Configs zu lesen
    import csv #Um CSV Datein zu verwenden
    import os #Um verschiedene Betriebssystem Operationen durchzuführen
    import hashlib #Um Hashes zu berechnen
    import sys #um die Abhängigkeiten zu instalieren
    import base64
    from collections import OrderedDict
    import atexit #um die datein noch beim stop verschlüsselt werden
    import shutil #Um ganze Pfade reqursiv zu löschen.

    try: 
        import requests
        import cryptography
        from cryptography.fernet import Fernet

    except Exception:
        print("Einige abhängigkeiten sind nicht installiert, versuche sie in 10 Sekunden zu installieren. \n \
Zum abbrechen CTRL+C drücken.")
        time.sleep(10)

        try:
            print(sys.executable)
            subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            import requests
            import cryptography
            from cryptography.fernet import Fernet

            print("requirements wurden installiert")

        except Exception:
            print(Exception, os.error)
            print("Es ist ein Fehler aufgetreten die Abhängigkeiten zu installieren versuche es manuell mit \"pip install -r requirements.txt\"")
        
    main()