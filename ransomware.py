import cryptography
import pathlib,os, secrets, base64, getpass
from cryptography.fernet import Fernet
import cryptography.fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# step 1 : Generate the salt from the secrets module
def derive_salt(size=16):
    return secrets.token_bytes(size)

# step 2 : generates the key using Scrypt module

def generate_key(password, salt):
    # we generate the key from the password and salt
    kdf = Scrypt(salt=salt, length=32, r=8, n=2**14, p=1)
    return kdf.derive(password.encode())
"""where ;
        length = length of the key
        r = block size parameter
        n= block/cost of CPU
        p= parallezation parameter
"""


# step 3 : load the salt
def load_salt():
    # load the salt from salt.salt open
    return open("salt.salt", "rb").read()


# step 4 : generate the key using salt and password
def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    """generates  the key from a 'password' and 'salt'
        if load_existing_salt is true , it will load existing from the current directory salt.salt file
        if save_salt is True , it will generate new salt and save it as salt.salt
    """

    if load_existing_salt:
        # loads rhe existing salt
        salt = load_salt()
    elif save_salt:
        # generate salt
        salt = derive_salt(salt_size)
        # generates new salt file salt.salt
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)

    # now generate the key 
    derived_key = derived_key(salt, password)
    # encode the derived key using base64
    return base64.urlsafe_b64encode(derived_key)


# step 5 : Encrypt file

def encrypt_file(filename, key):
    # create an object of Fernet and pass the key
    f = Fernet(key)

    # open the file and read it contents
    with open(filename, "rb") as file:
        # read all the file data
        file_data = file.read()

        # now encrypt the data
        encrypted_data = f.encrypt(file_data)
        # overwrite the salt.salt file with the encrypted data
        with open(filename, "wb") as file:
            file.write(encrypted_data)

# step 6 : Decryt your files
def decrypt_file(filename, key):
    # create an object of Fernet and pass the key
    f = Fernet(key)

    # read all encrypted data
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    try:
        # decrypt the data
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("[!!!!] Invalid token, most likely incorrect password")
        return
    
    # overwite the salt.salt file with decrypted data
    with open(filename, "wb") as file:
        file.write(decrypted_data)

# step 7 ; Encrypt folders
def encrypt_folder(foldername, key):
    # if it is a folder, encryt all of it
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[**] Encrypting {child}")
            encrypt_file(child, key)
        elif child.is_dir():
            print(f"[**] Encrypting {child}")
            encrypt_folder(child, key)



def decrypt_folder(foldername, key):
    # if it's a folder, decrypt all of it
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[**] Decrypting {child}")
            decrypt_file(child, key)
        elif child.is_dir():
            print(f"[**] Decrypting {child}")
            decrypt_folder(child, key)

if __name__ =="__name__":
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
        raise TypeError("PLease specify whether you want to encrypt the file or decrypt it ")
    elif to_encrypt:
        if os.path.isfile(args.path):
            # if it is a file encrypt it
            encrypt_file(args.path, key)
        elif os.path.isdir(args.path):
            encrypt_folder(args.path, key)
    
    elif to_decrypt:
        if os.path.isfile(args.path):
            decrypt_file(args.path, key)
        elif os.path.isdir(args.path):
            decrypt_folder(args.path, key)

    else:
        raise TypeError("Please specify whether you want to encrypt or decrypt the file!!!")

 

 