# NAME Hung Nguyen
# EMAIL hunghn4@uci.edu
# STUDENT ID 26441523

# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from Profile import Post, Profile
from NaClDSEncoder import NaClDSEncoder
import json, os
from pathlib import Path
from copy import deepcopy


class NaClProfile(Profile):
    def __init__(self):
        # Public key to send to the server as well as to encrypt/decrypt message
        self.public_key = None
        # Private key to send to the server as well as to encrypt/decrypt message
        self.private_key = None
        # Public key concatenates private key
        self.keypair = None
        # Access attributes of parent class
        super().__init__()

        
    def generate_keypair(self) -> str:
        """
        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer. 
        """
        # Create a NaClDSEncoder object
        nacl_enc = NaClDSEncoder()
        # Create a keypair
        nacl_enc.generate()
        #Split the keypair to get public, private keys and assign them to class attributes
        self.keypair = nacl_enc.keypair
        self.public_key = nacl_enc.keypair[:44]
        self.private_key = nacl_enc.keypair[44:]
        
        return self.keypair

    
    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.
        """
        # Check if input type is str
        if type(keypair) != str:
            print('ERROR!! Use make sure the type of keypair is string')
        else:
            # Check if length of keypair is 88   
            if len(keypair) != 88:
                print('ERROR!! Look like this keypair is not in correct format. It should have 88 characters')
            else:
                self.keypair = keypair
                self.public_key = keypair[:44]
                self.private_key = keypair[44:]


    def _encrypt_decrypt(self, crypto_type:str, public_key:str, entry:str):
        """
        This method helps avoid code repetition when encrypting/decrypting entries
        Firstly, creating a NaClDSEncoder object. Then creating publicKey, privateKey, objects
        Box object is then created. This is the main component to encrypt/decrypt entries
        """
        nacl_enc = NaClDSEncoder()
        try:
            pKey = nacl_enc.encode_public_key(public_key)
            prvKey = nacl_enc.encode_private_key(self.private_key)
            box_obj = nacl_enc.create_box(prvKey, pKey)
        
        # Perform encryption or decryption based on the the param: crypto_type
            if crypto_type == 'encrypt':
                encr_msg = nacl_enc.encrypt_message(box_obj, entry)
                return encr_msg

            elif crypto_type == 'decrypt':
                decr_msg = nacl_enc.decrypt_message(box_obj, entry)
                return decr_msg
        except:
            print('ERROR!! Invalid public or private key to perform encryption/decryption')

        
    def add_post(self,post:Post) -> None:
        """
        Encrypt an entry then add it to the object
        """
        try:
            encr_msg = self._encrypt_decrypt('encrypt', self.public_key, post.entry)
        except:
            print('ERROR!! Make sure to use a post object')
        else:
            post.set_entry(encr_msg)
            super().add_post(post)


    def get_posts(self):
        """
        Make a deep copy of ._post to ensure that all attributes, and data collections are copied
        Then decrypt all the entries in the new copy
        """
        decrypted_posts = deepcopy(self._posts)
        for post in decrypted_posts:
            post.entry = self._encrypt_decrypt('decrypt', self.public_key, post.entry)

        return decrypted_posts


    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the current instance of Profile with data stored in a DSU file.
        Since the new Profile class has additional keypair attribute, load_profile is re-written
        """
        # Remove all previous posts before loading the new profile          
        while len(self._posts) > 0:
            self._posts.pop()
                  
        p = Path(path)
        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.keypair = obj['keypair']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except:
                print('ERROR!! Cannot load the profile from the above file')
        else:
            print('ERROR!! This file does not exist or not in .dsu format')
            
            
    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides
        """
        # Check if input type is str
        if type(public_key) != str:
            print('ERROR!! Use make sure the type of pulic key is string')
        else:
            # Check if length of public key is 44   
            if len(public_key) != 44:
                print('ERROR!! Look like this public key is not in correct format. It should have 44 characters')
            else:
                return self._encrypt_decrypt('encrypt',public_key, entry)