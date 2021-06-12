#!/usr/bin/env python3

from ntpath import join
import os
from re import S
import hashlib
import base64
from cryptography.fernet import Fernet
import time

global workingpath
workingpath = os.path.dirname(os.path.realpath('__file__')) #Pfad in der die Datei ausgefürt wird



def generiere_schluessel(datei):
    """
    Generiert einen 32-Byte Base64 encodierten String aus dem Hash einer angegebenen Datei
    """
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
    with open(dateipfadvoher, "rb") as datei:
        # Lese die Datei
        datei_data = datei.read()
    # verschlüssele die Daten
    encrypted_data = f.encrypt(datei_data)
    # speichere die verschlüsselte Datei
    with open(dateipfadnachher, "wb") as datei:
        datei.write(encrypted_data)

def entschluessele(dateipfadvoher,dateipfadnachher,schluessel):
    """
    Entschlüsselt die Datei im Angegebenen Pfad mit den angegebenen Schlüssel.
    """
    f = Fernet(schluessel)
    with open(dateipfadvoher, "rb") as datei:
        # read the encrypted data
        encrypted_data = datei.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original datei
    with open(dateipfadnachher, "wb") as datei:
        datei.write(decrypted_data)


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
        entschluessele(voher[i],nachher[i],schluessel)



print("Achtung dies entschlüsselt deine Daten, und zeigt deine Schlüssel. Stelle sicher das niemand Schaut!")
print("Zum abbrechen \"STRG + C \" drücken.")
for i in range(4):
    time.sleep(1)
    print(3 - i)
    
print("Generiere deinen Key...")
schluessel = generiere_schluessel(os.path.join(workingpath,"config","credentials.json"))

print("Dein Schlüssel:")
print("-----BEGIN OF KEY -----")
print(schluessel)
print("-----END OF KEY -----")
print("RAW: " + str(base64.urlsafe_b64decode(schluessel)))


print("Entschlüssele Datein...")


if not (os.path.exists(os.path.join(workingpath,"speicher"))):
    print("Es gibt keine Daten zum entschlüsseln.")
os.makedirs(os.path.join(workingpath,"do_not_share") , exist_ok=True)

try:
    entschluessele_pfad(os.path.join(workingpath,"speicher"),os.path.join(workingpath,"do_not_share"),schluessel)
    print("Datein entschlüsselt nach \"" + os.path.join(workingpath,"do_not_share") + "\" !")
except(Exception):
    print("Die Datein konnten nicht entschlüsselt werden")
finally:
    print("Danke fürs nutzen!")

print("Wenn du die Datein in /cache und /do_not_share nicht mehr benötigst lösche sie.")
