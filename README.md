
# IServHelfer

![Logo](https://upload.oppisoft.de/x/Kry3WJ08fNuGY1ZX2Wm8R.svg)

[![Python application](https://github.com/Max-42/IServHelfer/actions/workflows/python-app.yml/badge.svg)](https://github.com/Max-42/IServHelfer/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/Max-42/IServHelfer/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Max-42/IServHelfer/actions/workflows/codeql-analysis.yml)

## Was ist der "IServ Helfer"?

Der **IServHelfer** ist ein [Python](https://www.python.org/) Programm, mit dem die automatisierte Integration mit [IServ](https://iserv.de/portal/zielgruppen) vereinfacht werden soll.
Mit dem **IServHelfer** können Aufgaben aus dem [IServ Aufgaben Modul](https://iserv.de/doc/modules/exercise/) an einen Discord Webhook gesendet werden.

[Webhooks Erklärung](https://www.dev-insider.de/was-ist-ein-webhook-a-996681/)
[Discord Webhooks](https://support.discord.com/hc/de/articles/228383668-Einleitung-in-Webhooks)

## Woher die Idee?

Das Ganze ist ein Schulprojekt daher auch die Idee die unsere Schulplattform (IServ) so zu automatisieren, sodass automatisiert Pushmitteilungen an bestimmte dritte Dienste gesendet werden können.

## Installation

### Forken

Erstelle eine Fork in deinem Github Account, dazu einfach oben rechts auf "Fork" klicken.

![Fork erstellen](http://upload.oppisoft.de/x/EP1I21qdslpMYb2LKFbFY.png)

### Secrets zur Anmeldung erstellen

Lege ein [Secret](/settings/secrets/actions) mit dem Namen CREDENTIALS_JSON mit dem Inhalt:

```json
    {
    "host": "deine-schule.de/iserv/",
    "username": "VORNAME.NACHNAME",
    "password": "DEINPASSWORT",
    "discord_webhook": "https://discord.com/api/webhooks/SERVERID/XXXXXXXX"
    }
```

an, und kopiere in das Secret Feld, dann solltest du..

- Deine IServ Adresse (ohne https://) ``` "deine-schule.de/iserv/" ```
- Deinen IServ Benutzernamen (Es kann sein das dies nicht überall vorname.nachname ist. ) ``` "VORNAME.NACHNAME" ```
- Deinen IServ Passwort: ``` "DEINPASSWORT" ```
- Und deinen Discord Webhook: ``` "https://discord.com/api/webhooks/SERVERID/XXXXXXXX" ``` [Hilfe zu Discord-Webhooks](https://support.discord.com/hc/de/articles/228383668-Einleitung-in-Webhooks)

... anpassen **hiermit verstößt man je nach Schule gegen die Nutzungsrichtlinien, da du so dein Passwort "Teilst"**

[Hilfe zu Secrets](https://docs.github.com/de/actions/reference/encrypted-secrets)

### Fertig

Jetzt wird mit hilfe von [GitHub Runnern](https://docs.github.com/de/actions/using-github-hosted-runners/about-github-hosted-runnersS) alle 15 Minuten das Pythonskript ausgeführt.
Die Änderungen durch das Skript werden automatisch mit deinem GitHub Secret verschlüsselt gespeichert, und beim nächsten Ausführen wieder entschlüsselt.

# Vorgehensweise

Das Projekt ist in Zusammenhang mit einem Schulprojekt an der [Friedrich-List-Schule](https://www.fls-hi.de/) entstanden, und wurde teils in der Schule und, teils zu Hause von mir geschrieben.

## Die Idee

Meine Idee war, mithilfe eines Python Scripts die Aufgaben aus dem IServ Aufgaben Modul an Drittanbieter zu senden.

Vorteile | Kritikpunkte
-------- | --------
Es ist so einfacher den Überblick zu Behalten   | Die Daten werden mit dritten wie z.B. Discord oder GitHub geteilt.
Mit GitHub kann das Projekt ohne extreme Kenntnisse **kostenlos** gehostet werden   | Die Daten werden zwar verschlüsselt, und gelöscht nach der Abfrage aber die Secrets zum Entschlüsseln hat GitHub auch.
Kostenlos - Ein GitHub Konto ist kostenlos, so bekommt jeder die Möglichkeit das Programm z.B. automatisch alle 15 Minuten auf Microsofts Servern laufen zu lassen.| Im falle eines Hackes oder Leakes der __credentials.json__ oder dem __CREDENTIALS_JSON__ Secret können alle Daten (auch alte) entschlüsselt werden.
OpenSource - | Je nach Schule verstößt man so gegen die Nutzungsverträge die man ggf. unterschrieben hat.

### Warum werden nur so wenig Infos gesendet?

Das ist Absicht, die Schulplattformen wie IServ gibt es nicht ohne Grund. Die IServ Server laufen meist auf Servern der Schulen und werden dementsprechend nicht mit dritten geteilt. Das Schützt die Privatsphäre. Mir ist Privatsphäre wichtig daher werden Informationen wie Anhänge/ Dateien der Aufgaben oder weitere Informationen nicht mit gesendet.

Ein großes Problem bleibt aber weiter bestehen, und zwar das man die Zugangsdaten zu seinem IServ Account mit GitHub "teilt". Kostenlos hat halt auch immer seine Nachteile. Daher ist ein Docker-Image in Planung, welches man dann mit nur einem Befehl zum Laufen bringen kann (vorausgesetzt [Docker](https://www.docker.com/) ist installiert.)

## Abhängigkeiten

Ich habe Abhängikeiten wie:

- [json](https://docs.python.org/3/library/json.html)
- [csv](https://docs.python.org/3/library/csv.html)
- [os](https://docs.python.org/3/library/os.html)
- [hashlib](https://docs.python.org/3/library/hashlib.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [base64](https://docs.python.org/3/library/base64.html)
- [OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
- [shutil](https://docs.python.org/3/library/shutil.html)

und die Python Pakete:

- [requests](https://pypi.org/project/requests/)
  - [**Requests**](https://docs.python-requests.org/en/master/) habe ich genutzt, um [HTTP](https://de.wikipedia.org/wiki/Hypertext_Transfer_Protocol)-Anfragen zu Senden um so mit den Webservern von unserem Schul-IServ und z.B Discord komunizieren zu können.
- [cryptography (Fernet)](https://pypi.org/project/cryptography/)
  - [**Fernet**](https://cryptography.io/en/latest/fernet/) habe ich genutzt, um die Daten die gespeichert bleiben sollen zu verschlüsseln.
    - Die Daten werden verschlüsselt um diese dann mithilfe eines Git-Commits auf GitHub (öffentlich, aber ja dann verschlüsselt) hochzuladen.
    - Hochgeladen werden sie damit sie später wieder verwendet werden können. Um die gleiche Benachrichtigung  nicht zweimal zu senden.

## Vorgehen

Ich habe als ich die Idee hatte, habe ich den HTTP-Traffic zwischen IServ und dem Browser mit [Burp Suite](https://portswigger.net/burp) angeschaut. Und mir Notizen über Request Header und Body gemacht,
sodass ich später HTTP-Anfragen mithilfe von dem [Python Paketes "requests"](https://pypi.org/project/requests/) nachstellen kann.

Ich bin nach dem __Code and Fix__ Vorgehensmodell vorgegangen,
welches recht chaotisch aber für mich intuitiv war da ich so in der Vergangenheit auch in Programmierprojekten so vorgegangen bin.

## Fazit

Ich bin mit dem Projekt zufrieden, aber es gibt sicher noch vieles was verbessert werden kann dazu zählen zum Beispiel: Eine Bessere Verschlüsselung, eine einfachere Installation, oder übersichtlicherer Code.

## Quellen

Die Quellen zu den Hilfeartikeln sind alle direkt verlinkt, aber hier noch einmal zusammengefasst.

### Aufgerufen am 6/13/2021

- Hilfeseiten
  - [Hilfe zu Secrets](https://docs.github.com/de/actions/reference/encrypted-secrets)
  - [IServ](https://iserv.de/portal/zielgruppen)
  - [IServ Aufgaben Modul](https://iserv.de/doc/modules/exercise/)
  - [Webhooks Erklärung](https://www.dev-insider.de/was-ist-ein-webhook-a-996681/)
  - [Discord Webhooks](https://support.discord.com/hc/de/articles/228383668-Einleitung-in-Webhooks)
  - [Docker](https://docs.docker.com/)
- Python Abhängikkeiten
  - [json](https://docs.python.org/3/library/json.html)
  - [csv](https://docs.python.org/3/library/csv.html)
  - [os](https://docs.python.org/3/library/os.html)
  - [hashlib](https://docs.python.org/3/library/hashlib.html)
  - [sys](https://docs.python.org/3/library/sys.html)
  - [base64](https://docs.python.org/3/library/base64.html)
  - [OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
  - [shutil](https://docs.python.org/3/library/shutil.html)
- Python Pakete
  - [requests](https://pypi.org/project/requests/)
  - [cryptography (Fernet)](https://pypi.org/project/cryptography/)
- Software
  - Verwendete Programmiersprache [Python](https://www.python.org/)
  - Containervirtualisierung [Docker](https://www.docker.com/)
  - Netzwerkanalyse-Werkzeugkasten [Burp Suite](https://portswigger.net/burp)

- Sonstige
  - HTML der Dokumentation erstellt mit der [GitHub Markdown API](https://docs.github.com/en/rest/reference/markdown)
  - CSS der Dokumentation: [Primer CSS](https://github.com/primer/css/tree/main/src/markdown)
  - [HTTP](https://de.wikipedia.org/wiki/Hypertext_Transfer_Protocol)
  - Die Schule auf die ich gehe: [Friedrich-List-Schule](https://www.fls-hi.de/)
