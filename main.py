#!/usr/bin/env python3

from sys import executable #Um dependencies zu installiern.

import json #Um die Configs zu lesen


def main():
   pass





    

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

