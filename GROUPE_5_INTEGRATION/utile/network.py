# coding: utf8
import socket
import pickle
import sys
from random import randint
from Cryptodome.Util.number import getPrime


def start_serv(ip, port):

    """
    Création du serveur
    :param ip: crée le serveur sur l'ip envoyée
    :param port: crée le serveur sur le port envoyé
    :return: renvoie le socket
    """
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)   # Récupération du socket
    s.bind((ip, port))                                                  # Lisaison du socket et de l'ip et port
    s.listen(1)                                                         # Le serveur écoute

    data, addr = s.accept()                                             # Récupération du socket final et de l'addresse
    #print(f"Connected to {ipaddress.IPv4Address(addr[0])}:{addr[1]}")

    return data                                                         # Renvoies le socket


def connect(ip, port, secured):

    """
    Connexion à un serveur lancé
    :param secured:
    :param ip: ip du serveur cible
    :param port: port du serveur cible
    :return: renvoie le socket
    """
    try:

        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        s.connect((ip, port))
        if secured:
            dict_g_p = [randint(9, 99), getPrime(12)]
            return s, dict_g_p
        else:
            return s
    except socket.error as e:
        print(f"Error connexion", {e})
        return None, None


def send_message(s, message, ip, port):

    """
    Fonction d'envois du message au serveur spécifié
    :param s: socket
    :param message: chaîne de charactère
    :param ip: IP du serveur cible
    :param port: Port du serveur cible
    """

    msg = pickle.dumps(message)                     #Sérialisation du message

    header = '{0:080b}'.format(sys.getsizeof(msg))  #Création du header
    msg = header.encode("windows-1252") + msg       #Concaténation du header et du message (windows-1252 --> ASCII étendue)

    s.sendto(msg, (ip, port))                       #Envois du message


def receive_message(s):

    """
    Reception du message sur le socket
    :param s: socket du serveur
    :return: renvoies le message "unpickle"
    """
    s.settimeout(None)

    buffer = s.recv(80)                             #Reception du header
    buffer = int(buffer.decode(), 2)                #Transforme le header reçu en entier (précédemment binaire)

    message = s.recv(buffer * 8)                    #Récupération complète du message
    message = pickle.loads(message)                 #Unpickle le message
    return message
