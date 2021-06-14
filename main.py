#!/usr/bin/env python3

from base64 import encode, urlsafe_b64decode
import os



workingpath = os.path.dirname(os.path.realpath('__file__')) #getting current path

def initialize():
    global logging
    logging = os.getenv('logging', True)

    global schluessel
    schluessel = generiere_schluessel(os.path.join(workingpath,"config","credentials.json"))

    atexit.register(verschluessele_pfad ,"cache","speicher",schluessel)
    
    #wenn schon Daten gespeichert worden sind werden diese entschlüsselt.
    if(os.path.isfile(os.path.join(workingpath,"speicher","aufgaben.json"))):
        entschluessele_pfad("speicher","cache",schluessel)

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

    #Lege benötigte Ordner an.
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
            eintrag = OrderedDict()
            for feld in feldnamen:
                eintrag[feld] = zeile[feld]
            eintraege.append(eintrag)
    
    ausgabe = {
        "Aufgaben": eintraege
    }
    tempjsoncache = os.path.join(workingpath, 'cache' , 'aufgaben.json')

    #Schreibt die JSON Datei auf die Festplatte.
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
    
    logger("Lese Konfiguration...")

    # Einstellungs Datei anlegen
    if not os.path.isfile(settingsfile): 
        logger("Die Einstellungsdatei kann nicht gefunden werden, eine neue wird erstellt...")
        config = {"_comment": "Stelle sicher, dass du die korrekte JSON-Syntax benutzt.", "logging": "True", "protocol": "https://"}

        with open(settingsfile, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            f.close
        
        print("WARNUNG - Es wurde eine Einstellungsdatei für dich angelegt, die richtigen Einstellungen sind noch nicht gegeben.")
        

    #Zugangsdaten Datei anlegen
    if not os.path.isfile(credentialsfile):
        logger("Die Zugangsdatendatei kann nicht gefunden werden, eine neue wird erstellt...")
        config = {"_comment": "Stelle sicher, dass du diese Datei NICHT teilst!  Und stelle sicher, dass du die korrekte JSON-Syntax benutzt.", "host": "deine-schule.de/iserv/", "username": "vorname.nachname", "password":"yOUr-SEcuRe-P4s5w0RD","discord_webhook": "https://discord.com/api/webhooks/XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}

        with open(credentialsfile, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            f.close
        
        print("Stoppe, weil eine Zugangsdatendatei für dich angelegt wurde. Die richtigen Zugangsdaten sind dort noch nicht enthalten.")
        exit(1)

    
    if logger():
        with open(settingsfile, 'r' ,encoding='utf-8') as f:
            global settings
            settings = json.load(f)
            f.close
        # logger("Settings: " + str(settings))

    with open(credentialsfile, 'r', encoding='utf-8') as f:
        global credentials
        credentials = json.load(f)
        f.close
    
    if (hashlib.sha1(str(credentials).encode('utf-8')).hexdigest()) == "a8a15dd72b6e1cddb4f238a64f1b4c87263a33d9":
        print("You are using the default credentials file please make sure to fill out this file.")
        exit(1)
    
    if(hashlib.sha1(str(settingsfile).encode('utf-8')).hexdigest())== "720e0948396da23020a348be4d5a17dc44829ae1":
        print("You are using the default settings file please make sure to fill out this file.")
    store_data(ladeaufgaben())

    jsonhandler()

    sender()

    print("Danke fürs nutzen!")
    cleanup()
    

def ladeaufgaben():
    url = settings['protocol'] + credentials['host'] +"app/login"
    querystring = {"target":"/iserv/exercise.csv?sort[by]=enddate&sort[dir]=DESC?"}
    payload = "_username=" + credentials['username'] + "&_password=" + credentials['password']
    headers = {
    "User-Agent": "IServHelfer/0.1 (+https://github.com/Max-42/IServHelfer)",
    "Content-Type": "application/x-www-form-urlencoded"
    }
    antwort = request("POST", url=url, headers=headers, payload=payload , querystring= querystring)
    # print("Text: " + antwort)
    return antwort
   
def request(method, url, headers ,payload='', querystring='', json='', timeout=(10,30)):
    try:
        print("HTTP " + method + " Anfrage an " + url[:11] + "***") #Zensiert um den IServ Schulserver auf z.B GitHub-runners geheim zu halten. 
        response = requests.request(method, url, data=payload, headers=headers, params=querystring, json=json, timeout=timeout) #timeout sets a connection timeout of 10 Sec. And a read timeout of 30 sec.
        print(response.text)
        return response.text

    except Exception:
        if not logger():
            print("Die Anfrage an den Server ist fehlgeschlagen.")
        logger("The request failed:")
        logger(sys.exc_info()[1])

def sendtodiscord(aufgabe,von,bis,link):
    """
    Sendet eine Nachicht an einen in der Config interlegten webhook.
    """
    if credentials["discord_webhook"] == "":
        return
    method = "POST"
    url = credentials['discord_webhook']
    querystring = {"payload":"test"}
    payload = {
        "content": "Neue Aufgabe: **" + aufgabe + "**",
        "embeds": [
            {
                "color": 	1136765, #Decimal code für hex #11587d
                "footer": {"text": "IServHelfer 🥶 github.com/Max-42/IServHelfer"}, 
                "thumbnail": {"url": "http://upload.oppisoft.de/x/gYt750AkJeW3Srny66I6J.png"}, #IServHelfer Logo
                "author": {
                    "name": "Zur Aufgabe", 
                    "url": link
                },
                "fields": [
                    {
                        "name": "Aufgabe",
                        "value": aufgabe
                    },
                    {
                        "name": "Von",
                        "value": von,
                        "inline": True
                    },
                    {
                        "name": "Bis",
                        "value": bis,
                        "inline": True
                    }
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    # print(method, url, payload, headers, querystring)
    request(method=method, url=url, headers=headers, querystring=querystring, json=payload,)

def jsonhandler():
    aufgaben = {}
    gesendet= {}
    # Pfad zu der daten.json
    datenpfad = os.path.join(workingpath,"cache","daten.json")
    try:
        with open(datenpfad,"r") as f:
            datendatei = json.load(f)
            aufgaben = datendatei["Aufgaben"]
            gesendet = datendatei["Gesendet"]            
    except Exception as e:
        print("Es ist ein Fehler aufgetreten :")
        # print(e)
        print("Das sollte aber kein Problem sein.")
        with open(datenpfad,"w+") as f:
            aufgaben = {}
            gesendet= {}
            datenneu={"Aufgaben":aufgaben,"Gesendet":gesendet}
            json.dump(datenneu,f,indent=4)
        with open(datenpfad,"r") as f:
            datendatei = json.load(f)
            aufgaben = datendatei["Aufgaben"]
            gesendet = datendatei["Gesendet"]

        aufgaben = {}
        gesendet= {}
    datenneu={"Aufgaben":aufgaben,"Gesendet":gesendet}
    with open(os.path.join(workingpath,"cache","aufgaben.json"),"r") as f:
        data = json.load(f)

    for aufgabe in data["Aufgaben"]:
        if not aufgabe["Aufgabe"] == "Aufgabe":

            # Generiere einen Hash der Aufgabe, da wenn nur der Name abgefragt werden würden Aufgaben mit dem gleichen Namen nicht gesendet würden.
        
            summe = aufgabe["Aufgabe"] + aufgabe["Starttermin"] + aufgabe["Abgabetermin"] + aufgabe["Tags"] + aufgabe["Erledigt"] + aufgabe["Rückmeldungen"]
            summe = hashlib.md5(summe.encode('utf-8')).hexdigest()

            #Speichert die letzten 10 Zeichen des md5-Hashes aus der Aufgabe ab.
            aufgabe["summe"] = summe[:10]

            aufgaben[summe[:10]]=aufgabe
            
            try:
                if (gesendet[aufgabe["summe"]] == True):
                    gesendet[aufgabe["summe"]] = True
                else: gesendet[aufgabe["summe"]] = False
            except Exception as e:
                print("Fehler:")
                print(e)

            if aufgabe["summe"] in datendatei["Gesendet"]:
                print("")
            else:
                gesendet[aufgabe["summe"]]  = False
    datenneu={"Aufgaben":aufgaben,"Gesendet":gesendet}

    #Speichern
    with open(datenpfad, "w+") as f:
        json.dump(datenneu,f,indent=4)


def sender():
    with open(os.path.join(workingpath,"cache","daten.json")) as f:
        data = json.load(f)
    for nachicht in data["Gesendet"]:
        if not (data["Gesendet"][nachicht]):
            time.sleep(3)

            data["Gesendet"][nachicht]= True
            
            # print(data["Aufgaben"][nachicht]["Aufgabe"])
            if(data["Aufgaben"][nachicht]["Aufgabe"] == "\ufeffAufgabe"):
                logger("Überspringe leere Aufgabe.")
            else:
                sendtodiscord(data["Aufgaben"][nachicht]["Aufgabe"],data["Aufgaben"][nachicht]["Starttermin"],data["Aufgaben"][nachicht]["Abgabetermin"],settings["protocol"]+credentials["host"]+"exercise")

    with open(os.path.join(workingpath,"cache","daten.json"),"w") as f:
        json.dump(data,f,indent=4)



def cleanup():
    """
    Kümmert sich um die Verschlüsselung und anschließende Löschung der unverschlüsselten Dateien.
    Damit diese nicht im Git-Commit mit Committet und gepushed werden, da die Daten sonst so geleakt werden würden.
    """
    # sendtodiscord("Test","1","2","https://fls-hi.de/")
    verschluessele_pfad("cache","speicher",schluessel)
    # time.sleep(10)
    shutil.rmtree(os.path.join(workingpath,"cache"))
    shutil.rmtree(os.path.join(workingpath,"config"))

if __name__ == '__main__':
    #imports:
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

    #nicht inklusive (müssen mit pip nachinstalliert werden.)
    try: 
        import requests
        import cryptography
        from cryptography.fernet import Fernet

    except Exception:
        print("Einige abhängigkeiten sind nicht installiert, versuche sie in 10 Sekunden zu installieren. \n \
                Zum abbrechen CTRL+C drücken.")
        time.sleep(10)

        try:
            #print(sys.executable)
            subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            import requests
            import cryptography
            from cryptography.fernet import Fernet

            print("Abhängigkeiten wurden installiert")

        except Exception:
            print(Exception, os.error)
            print("Es ist ein Fehler aufgetreten die Abhängigkeiten zu installieren versuche es manuell mit \"pip install -r requirements.txt\"")
        
    main()