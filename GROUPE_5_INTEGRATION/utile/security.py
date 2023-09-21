from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import hashlib
from utile.network import send_message, receive_message
from Cryptodome.Util.number import getRandomInteger
import time


def AES_GCM_encrypt(plain_text, DiffiHellman_key):

    #Creation salt
    salt = get_random_bytes(AES.block_size)

    #Creation key private
    private_key = hashlib.scrypt(DiffiHellman_key.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    #Creation cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text  (bytes(plain_text, 'utf-8'))
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))

    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8'),
    }


def AES_GCM_decrypt(enc_dict, DiffiHellman_key):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict["nonce"])
    tag = b64decode(enc_dict["tag"])

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(DiffiHellman_key.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted


def send_Diffie_Hellman_exchange_key(socket,  ip, port, g_and_p):

    send_message(socket, g_and_p, ip, port)
    g, p = g_and_p

    # Génération d'un chiffre aléatoire secret
    secret_number = getRandomInteger(12)

    # Création d'une clé publique
    public_key = (g ** secret_number) % p

    # Envoie de la clé publique vers le destinataire
    print("Échange de la clé en cours...")
    time.sleep(3)
    send_message(socket, public_key, ip, port)  #"127.0.0.1", 8331)

    # Reception de la clé publiques
    dest_public_key = receive_message(socket)

    # Création du secret commun grâce aux clés reçues
    computer_key = (dest_public_key**secret_number) % p

    common_secret = hashlib.sha256(str(computer_key).encode()).hexdigest()

    return common_secret


def receive_Diffie_Hellman_exchange_key(socket,  ip, port):

    # Chiffre publiques
    g, p = receive_message(socket)

    # Génération d'un chiffre aléatoire secret
    secret_number = getRandomInteger(12)

    # Création d'une clé publique
    public_key = (g ** secret_number) % p

    # Reception de la clé publiques
    dest_public_key = receive_message(socket)

    # Envoie de la clé publique vers le destinataire
    print("Échange de la clé en cours...")
    time.sleep(3)
    send_message(socket, public_key, ip, port)  #"127.0.0.1", 8331)

    # Création du secret commun grâce aux clés reçues
    computer_key = (dest_public_key**secret_number) % p

    common_secret = hashlib.sha256(str(computer_key).encode()).hexdigest()

    return common_secret


def crypt_files():
    print()


def uncrypt_files():
    print()