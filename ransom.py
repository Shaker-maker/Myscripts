import pathlib, os, secrets, base64, getpass
import cryptography
from cryptography.fernet import Fernet
import cryptography.fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# Deriving the key from a Password
"""
key derivations functions need random bits added to the password before it is hashed, these
bits are called salts which strengthen security and protect against
brute-force and dictionary attacks

i will use secrets module
"""

def generate_salt(size=16):
    """Generate the salt used for key derivation
    'size' is the length of the salt to generate"""
    return secrets.token_bytes(size)


""" secrets module instead of random coz secrets it is used to generate cryptographically strong 
random numbers suitable for password gen, salts, security tokens
"""

# step 2 :: Derive the key from the password and the salt

def derive_key(salt, password):
    """ derive the keay from the password using the passed salt

    """

    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())
    """
    32 is length of key
    n CPU/Memory cost parameter
    r Block size parameter
    p parallezation parameter


    """


# step 3 : load the previously generated salt
def load_salt():
    # load the salt from salt.salt file
    return open("salt.salt", "rb").read()


# step4 ; Derive a function that the key from a password

def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    """
    generates a key from a 'password' and the salt.
    if load_existing_salt is True, it wil loda the salt file from the current
    directory called salt.salt

    if save_salt is 'True' then it will generate a new salt and save it to salt.salt

    """

    if load_existing_salt:
        # load existing salt
        salt = load_salt()
    elif save_salt:
        # generate new salt and save it
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)

    # generate the key from the salt and the password
    derived_key = derive_key(salt, password)

    # encode it using base64 and return it
    return base64.urlsafe_b64encode(derived_key)



# after creating the keys we enter the fun part , the file encryption

def file_encrypt(filename, key):

    """Given a filename (str) and key (bytes) it encrypts file and writes it"""
    # make an object of fernet and pass the key
    f = Fernet(key)
    with open(filename, "rb") as file: 
        # read all the file data
        file_data = file.read()

        # encrypt data
        encrypted_data = f.encrypt(file_data)
        # write the encrypted file 
        with open(filename, "wb") as file:
            file.write(encrypted_data)


# step 6 file decryption
def file_decrypt(filename, key):

    f = Fernet(key)

    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    try:
    # decrypt the data
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("[!!] Invalid token, most likely the password is incorrect")
        return
    # overriride the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)



# step 7 ; Encrpt Folders

def folder_encrypt(foldername, key):
    
    # if it's a folder, encrypt the entire folder
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Encrypting {child}")
            file_encrypt(child, key)
        elif child.is_dir():
            folder_encrypt(child, key)

#step 8 : Decrypt the folder

def folder_decrypt(foldername, key):
    # if it's a folder, decrypt the entire folder
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Decrypting {child}")
            file_decrypt(child, key)
        elif child.is_dir():
            print(f"[*] Decrypting {child}")
            folder_decrypt(child, key)

# final step: Using argparse module to make our script as easily usable as possible from the command line:

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="File Encryptor Script with a Password")
    parser.add_argument("path", help="Path to encypt/decrypt, can be a file or an entire folder")
    parser.add_argument("-s", "--salt-size", help="if this is set, a new salt with the passed size is generated", type=int)
    parser.add_argument("-e", "--encrypt", action="store_true", help="Whether to encrypt the file/folder, only -e or -d can be specified")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Whether to encrypt/decrypt, only -e and -d can be specified")
    
    args = parser.parse_args()
    if args.encrypt:
        password = getpass.getpass("Enter the password for encryption: ")
    elif args.decrypt:
        password = getpass.getpass("Enter password you used for decryption: ")

    if args.salt_size:
        key = generate_key(password, salt_size=args.salt_size, save_salt=True)

    else:
        key = generate_key(password, load_existing_salt=True)
    to_encrypt = args.encrypt
    to_decrypt = args.decrypt

    if to_encrypt and to_decrypt:
        raise TypeError("PLease specify whether you want to encrypt the file or decrypt it> ")
    elif to_encrypt:
        if os.path.isfile(args.path):
            # if it is a file encrypt it
            file_encrypt(args.path, key)
        elif os.path.isdir(args.path):
            folder_encrypt(args.path, key)
    
    elif to_decrypt:
        if os.path.isfile(args.path):
            file_decrypt(args.path, key)
        elif os.path.isdir(args.path):
            folder_decrypt(args.path, key)

    else:
        raise TypeError("Please specify whether you want to encrypt or decrypt the file!!!")

 