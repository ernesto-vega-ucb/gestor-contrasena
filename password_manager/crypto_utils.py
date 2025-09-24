# crypto_utils.py

import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Función para derivar una clave AES de la contraseña maestra
def derive_key(password, salt):
    kdf = Scrypt(
        salt=salt,
        length=32, # Longitud de la clave AES-256
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Función para cifrar datos
def encrypt(data, key):
    # Genera un vector de inicialización aleatorio
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Rellena los datos para que sean múltiplos del tamaño de bloque
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def decrypt(data, key):
    """Descifra los datos usando AES en modo CBC."""
    # Extrae el vector, que son los primeros 16 bytes de los datos cifrados
    iv = data[:16]
    encrypted_data = data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Descifra los datos
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Elimina el relleno
    unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return unpadded_data.decode('utf-8')