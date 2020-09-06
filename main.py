import os
import pickle
import hashlib
import base64

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding
from database import Database


class AESCipher:

    def __init__(self, key): 
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw):
        raw = Padding.pad(raw, AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return Padding.unpad(cipher.decrypt(enc[AES.block_size:]), AES.block_size)


class PasswordManager:
    def __init__(self):
        self.database = None
        self.name = None
        self.aes = None

    def open(self, file, password):
        k = hashlib.sha256(password.encode('utf-8')).digest()

        with open(file, 'rb') as f:
            self.database = pickle.load(f)

            print(self.database)

            self.name = next(iter(self.database.keys()))

        salt = self.database['salt']
        key_hash = self.database['key']

        key = hashlib.pbkdf2_hmac('sha256', k, salt, 100000)

        if key_hash != hashlib.pbkdf2_hmac('sha256', hashlib.sha256(key).digest(), salt, 100000):
            self.database = None
            self.name = None

            print("Wrong Password")
        
        else:
            self.aes = AESCipher(key)

    def new(self, name, password):
        self.name = name

        k = hashlib.sha256(password.encode('utf-8')).digest()
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac('sha256', k, salt, 100000)
        
        key_hash = hashlib.pbkdf2_hmac('sha256', hashlib.sha256(key).digest(), salt, 100000)

        self.aes = AESCipher(key)

        self.database = {
            name: Database(),
            'key': key_hash,
            'salt': salt
        }

    def add_table(self, name):
        self.database[self.name].add_table(name, 'title', 'user', 'password', 'url', 'notes')

    def add_entry(self, table, title, user, password, url, notes):
        self.database[self.name].add(table, title=title, user=user, password=self.aes.encrypt(password.encode('utf-8')), url=url, notes=notes)

    def delete_table(self, name):
        self.database[self.name].delete_table(name)

    def delete_entry(self, name, index):
        self.database[self.name].delete_entry(name, index)

    def save(self, file):
        with open(file, 'wb') as f:
            pickle.dump(
                self.database, f
            )

    def out(self):
        if self.database:
            print(self.name)

            self.database[self.name].out()
                
        else:
            print("No Database open!")


class MemoryFile:
    pass


if __name__ == "__main__":
    manager = PasswordManager()

    # manager.new('MyDatabase', 'secret')

    # manager.add_table('General')

    '''
    manager.add_entry(
        table='General',
        title='GoogleDrive',
        user='HappyMeal',
        password='verysecure',
        url='drive.google.com',
        notes='this is my google drive!'
    )
    '''
    manager.open('database.txt', 'secret1')

    manager.out()

#    manager.save('database.txt')
