import os
import colorama
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib
import time
import keyboard
import sys


MAIN_MENU = f"""                                                        
                                         _____                    _____                         
                                        | __  |___ ___ ___ ___   |     |___ ___ ___ ___ ___ ___ 
                                        | __ -| .'|  _| . |   |  | | | | .'|   | .'| . | -_|  _|
                                        |_____|__,|___|___|_|_|  |_|_|_|__,|_|_|__,|_  |___|_|   Ver. 1.0
                                                                                   |___|        
                                                                                                   
                                                                            |
                                                                            |          <Options>
                                              :.                            |
                                            :P!7?7:                         |
                                            P!::^77?!                       |           1 ~> View Passwords
                                           ~P:::~!:.#G^                     |
                                          :P^::~!~.^BJB^                    |           2 ~> Add Password
                                         !5^::~!!:.JG?55                    |
                                     .^7J!::^~!!:.~BJ?G?                    |           3 ~> Remove Password
                                 .~7?7!^^^~!!!^..7GJ?JB.                    |
                               ^J?~^^^~!!!!^:..~5PJ?JB^ 77^                 |           4 ~> Visit Our Website
                              7Y^:^~!!!~^:.:~?55J?J5G~^5~^YY                |
                             ~P::~!!~^..:!Y55YJJY557.7Y^^~~JP               |           5 ~> Join Our Discord Server
                            .G^:^!!^..!5PYJJJYYJ7^.~Y!:^!!!!?5              |           
                            P7:^!!:.^PPJ?YPBGJ!~~7?!^^~!!!!^.PY             |           6 ~> Exit
                          ~5!:^~!:.~BY?JG5!~~~~~~^^^~!!!!~:.YP#.            |   
                     .:~7?7^:^~!^..BY?JBY~~!!!!!!!!!!!!!^.:5P5G             |            
                .^7??7!~^:^^~!!~..5P??GP~!!!!!!!!!!!!~^..7P5PJ              |          <Key Binds>
             .!?7~^^^^^~~!!!!~:..JGJ?5P::::::::::::...:75P5P^               |           
           .JJ~::^~~!!!!~~^:..:7P5??5B7!7??777!!!!!7?YPPP5~                 |            
         :5B~:^~!!!!~^:.:^!7JY5YJ?YGBPY555555555PPPPP5Y7:                   |           Ctrl + L ~> Log Out
        ?JP?:~!!!!^..^?Y555YYYYYP#GYJY5Y7~^^^~~!!~~:.                       |            
        B^55~!!!~..^5PYJY5YJ?!~7G5?YP7.                                     |           Ctrl + E ~> Exit (Recommended Instead Of Log Out)
        YY!PP7!~..7GY?5BJ~^^^!YPJYP?.                                       |            
         G7^~J5!.~BJ?5B5YY555YY55?.                                         |
         .P:.7GP5#GJJBGYYY555Y?^                                            |
          :PG5?YP?~JY?.:^^:.                                                |
           .55P5.                                                           |
             ..                                                             |
                                                                            |   


"""
def encryption(key, plaintext):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key.encode()), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return ciphertext

def decryption(key, ciphertext):
    cipher = Cipher(algorithms.AES(key.encode()), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode()

def logout_bind():
   login()

def exit_bind():
   sys.exit()

def main_cli():
    os.system("cls")
    os.system(f"title Bacon Manager v1.0 ~ Logged In As {username} ")
    os.system("mode con:cols=140 lines=42")
    print(colorama.Fore.LIGHTCYAN_EX + MAIN_MENU + colorama.Fore.RESET)
    opt = input(colorama.Fore.LIGHTCYAN_EX + "  BaconManager/Console/.. " + colorama.Fore.RESET)

    if opt == "":
       print(colorama.Fore.RED + "  !Invlid Option!" + colorama.Fore.RESET)
       time.sleep(1)
       main_cli()

    elif opt == "1":
       main_cli()

    elif opt == "2":
       main_cli()

    elif opt == "3":
       main_cli()

    elif opt == "4":
       main_cli()

    elif opt == "5":
       main_cli()

    elif opt == "6":
       exit()
       
    else:
       print(colorama.Fore.RED + "  !Invlid Option!" + colorama.Fore.RESET)
       time.sleep(1)
       main_cli()

    main_cli()

def main_gui():
    # Not Done
    input("Work In Progress")
    exit()

def login_creation():
    global key, username

    os.system("cls & title Bacon Manager v1.0 ~ Account Creation")
    print(colorama.Fore.RED + "\nYour username must be minimum 8 characters long!" + colorama.Fore.RESET)
    print(colorama.Fore.RED + "Your password must be minimum 8 characters long!\n" + colorama.Fore.RESET)
    username = input(colorama.Fore.LIGHTCYAN_EX + "Username ~> " + colorama.Fore.RESET)
    master_pass = input(colorama.Fore.LIGHTCYAN_EX + "Enter Your Master Password ~> " + colorama.Fore.RESET)
    second_entry = input(colorama.Fore.LIGHTCYAN_EX + "Re-Enter The Password ~> " + colorama.Fore.RESET) 
    if len(username) < 8:
      login_creation()
      print(len(username))
    if len(master_pass) < 8 or master_pass != second_entry:
      login_creation()
      print(len(master_pass))

    key = username[0:8] + master_pass[0:8]
    encrypted_password = encryption(key, master_pass)
    hash_password = hashlib.md5(encrypted_password).hexdigest()
    with open("UserData.txt", "w") as w:
       w.write(f"{username}:{hash_password}")
       w.close()

    if style == "cli":
       main_cli()
    if style == "gui":
       main_gui()

def login():
    global username

    os.system(f"title Bacon Manager v1.0 & mode con:cols=80 lines=16")
    os.system("cls")
    username = input(colorama.Fore.LIGHTCYAN_EX + "\nUsername ~> " + colorama.Fore.RESET)
    master_pass = input(colorama.Fore.LIGHTCYAN_EX + "Enter Your Master Password ~> " + colorama.Fore.RESET)

    if len(master_pass) < 8 or len(username) < 8:
      print(colorama.Fore.RED + "\n   !Invalid Login!" + colorama.Fore.RESET)
      time.sleep(2)
      login()

    key = username[0:8] + master_pass[0:8]
    encrypted_password = encryption(key, master_pass)
    hash_password = hashlib.md5(encrypted_password).hexdigest()

    with open("UserData.txt", "r") as r:
       userdata = r.read().split("\n")
       r.close()
    
    for user in userdata:
       if user.split(":")[0] == username and user.split(":")[1] == hash_password:
          if style == "cli":
             main_cli()
          elif style == "gui":
             main_gui()
             
    print(colorama.Fore.RED + "\n   !Invalid Login!" + colorama.Fore.RESET)
    time.sleep(2)
    login()

def boot():
    global style

    keyboard.add_hotkey('Ctrl+L', logout_bind)
    keyboard.add_hotkey('Ctrl+E', exit_bind)

    os.system(f"title Bacon Manager v1.0 & mode con:cols=80 lines=16")
    boot = input(colorama.Fore.LIGHTCYAN_EX + "Would you like to use CLI or GUI? " + colorama.Fore.RESET)
    if boot.lower() == "cli":
      style = "cli"
    elif boot.lower() == "gui":
      style = "gui"
    else:
      exit()

    if os.path.exists("UserData.txt"):
      new_user = False
      if os.path.exists("Passwords.txt"):
         pass
      else:
         with open("Passwords.txt", "w") as c:
            c.close()
    else:
      new_user = True
      with open("UserData.txt", "w") as c:
        c.close()
      if os.path.exists("Passwords.txt"):
         os.remove("Passwords.txt")
         with open("Passwords.txt", "w") as c:
            c.close()
      else:
        with open("Passwords.txt", "w") as c:
          c.close()
      login_creation()
    login()



if __name__=="__main__":
    boot()