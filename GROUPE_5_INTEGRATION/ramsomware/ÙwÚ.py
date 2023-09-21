import platform
import string
import sys
from ctypes import windll
from utile.network import connect, send_message
from utile.security import send_Diffie_Hellman_exchange_key, AES_GCM_encrypt


def get_disks():

    drive = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drive.append(letter)
        bitmask >>= 1
    return drive


def get_OS():
    return platform.system()


def get_computer_name():
    return platform.node()


def get_os_type():
    return sys.getwindowsversion()


def main():

    tuple_retour = connect("127.0.0.1", 8384, True)  # Récupère un tuple lors de la connexion au serveur
    socket = tuple_retour[0]  # La position 0 est le socket de connexion et la position 1
    g_p = tuple_retour[1]  # Est le g_p requis pour Dif_Hellman
    common_secret = send_Diffie_Hellman_exchange_key(socket, "127.0.0.1", 8384, g_p)  # Appel de la fonction et récupère la clé commune
    while True:
        message = input("Yes.")
        message = AES_GCM_encrypt(message, common_secret)
        send_message(socket, message, "127.0.0.1", 8384)


if __name__ == '__main__':
    print(get_disks())
