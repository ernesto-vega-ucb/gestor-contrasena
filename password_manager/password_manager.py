import os
import json
from .crypto_utils import derive_key, encrypt, decrypt # Importa las funciones del módulo de criptografía

class PasswordManager:
    def __init__(self, master_password):
        """Inicializa el gestor, derivando la clave de cifrado a partir de la contraseña maestra."""
        self.salt = self.load_salt()
        self.key = derive_key(master_password, self.salt)
        self.data_file = 'passwords.enc'
        self.passwords = self.load_passwords()

    def load_salt(self):
        """Carga el salt del archivo de configuración o crea una nueva si no existe."""
        salt_file = 'config.dat'
        if os.path.exists(salt_file):
            with open(salt_file, 'rb') as f:
                return f.read()
        else:
            salt = os.urandom(16)
            with open(salt_file, 'wb') as f:
                f.write(salt)
            return salt

    def load_passwords(self):
        """Carga y descifra el archivo de contraseñas. Retorna un diccionario."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_json = decrypt(encrypted_data, self.key)
            return json.loads(decrypted_json)
        return {}

    def save_passwords(self):
        """Cifra el diccionario de contraseñas y lo guarda en un archivo."""
        json_data = json.dumps(self.passwords)
        encrypted_data = encrypt(json_data, self.key)
        with open(self.data_file, 'wb') as f:
            f.write(encrypted_data)

    def add_password(self, service, username, password):
        """Cifra y añade una nueva contraseña al diccionario."""
        encrypted_password = encrypt(password, self.key).hex() # Cifra la contraseña individualmente
        self.passwords[service] = {
            'username': username,
            'password': encrypted_password
        }
        self.save_passwords()

    def get_password(self, service):
        """Descifra y retorna la contraseña de un servicio dado."""
        if service in self.passwords:
            encrypted_password = bytes.fromhex(self.passwords[service]['password'])
            return decrypt(encrypted_password, self.key)
        return None

    def list_passwords(self):
        """Retorna una lista de todos los servicios almacenados."""
        passwords_list = []
        for i, (service, data) in enumerate(self.passwords.items()):
            passwords_list.append({
            'id': i + 1,
            'servicio': service,
            'usuario': data['username']
        })
        return passwords_list

    def delete_password(self, service):
        """Elimina una contraseña del diccionario."""
        if service in self.passwords:
            del self.passwords[service]
            self.save_passwords()
            return True
        return False

    def change_master_password(self, new_master_password):
        """
        Cambia la contraseña maestra, recifrando todos los datos.
        """
        current_passwords = self.load_passwords()

        new_salt = os.urandom(16)
        new_key = derive_key(new_master_password, new_salt)

        reciphered_passwords = {}
        for service, data in current_passwords.items():
            old_encrypted_pw = bytes.fromhex(data['password'])
            decrypted_pw = decrypt(old_encrypted_pw, self.key)

            new_encrypted_pw = encrypt(decrypted_pw, new_key).hex()
            reciphered_passwords[service] = {
                'username': data['username'],
                'password': new_encrypted_pw
            }

        self.salt = new_salt
        self.key = new_key
        self.passwords = reciphered_passwords
        self.save_passwords()
        self.save_salt()

    #Guarda el nuevo salt en el archivo de configuración
    def save_salt(self):
        salt_file = 'config.dat'
        with open(salt_file, 'wb') as f:
            f.write(self.salt)