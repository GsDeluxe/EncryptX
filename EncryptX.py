#----------------------------------Modules----------------------------------#

import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import keyboard
import pyperclip
import random
import base64
import tkinter
from tkinter import ttk
import customtkinter
import ctypes
import gc
import sys
import pygetwindow as gw
from CTkMessagebox import CTkMessagebox
import pyautogui
import keyboard

#----------------------------------Constants----------------------------------#

version = "v1.0.4a"
SW_HIDE = 0
SW_SHOW = 5

#----------------------------------Functions----------------------------------#

class CryptoHandler():
   def generate_key(self, password):

      salt = b'~4\xb43\xf6.\xc16P\xc7C\x84\n\xc0\x9e\x96'

      kdf = PBKDF2HMAC(
         algorithm=hashes.SHA256(),
         length=32,
         salt=salt,
         iterations=1000,
         backend=default_backend()
      )

      key = kdf.derive(password.encode('utf-8'))

      return key

   def encryption(self, key, plaintext):
      try:
         iv = os.urandom(16)

         padder = padding.PKCS7(algorithms.AES.block_size).padder()
         plaintext_padded = padder.update(plaintext) + padder.finalize()

         cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

         encryptor = cipher.encryptor()
         ciphertext = encryptor.update(plaintext_padded) + encryptor.finalize()

         encoded_text = base64.b64encode(iv + ciphertext)

         return encoded_text.decode("utf-8")

      except Exception as e:
         print("\nError Encrypting! " + str(e))

   def decryption (self, key, ciphertext_encoded):
      try:
         ciphertext = base64.b64decode(ciphertext_encoded)

         iv = ciphertext[:16]

         cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
         decryptor = cipher.decryptor()

         decrypted_padded = decryptor.update(ciphertext[16:]) + decryptor.finalize()

         unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
         decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

         return decrypted

      except Exception as e:
         print("\nError Decrypting! " + str(e))

# Keybinds #

def lock_bind():
   try:
      del key
   except:
      pass

   gc.collect()

   os.execl(sys.executable, sys.executable, *sys.argv)

def exit_bind():
   try:
      root.destroy()
   except:
      pass
   try:
      login.destroy()
   except:
      pass

   gc.collect()
   sys.exit(0)

# Password Related #

def get_data():
   ready_data = []

   if os.path.isfile("Passwords.encryptx") != True:
      with open("Passwords.encryptx", "w") as w:
         w.close()
      
   with open("Passwords.encryptx", "rb") as read:
      split_data = read.read().split(b"\n")
      read.close()

   for data in split_data:
         if data:
            url_or_program, user, password = data.split(b"04n$b3e0R5K*")
            url_or_program, user, password = base64.b64decode(url_or_program), base64.b64decode(user), base64.b64decode(password)
            url_or_program = crypto_handler.decryption(key, url_or_program).decode()
            user = crypto_handler.decryption(key, user).decode()
            password = crypto_handler.decryption(key, password).decode()
            rating = password_rating_check(password)
            ready_data.append([url_or_program, user, password, rating]) 

   for ind, x in enumerate(ready_data):
      x.insert(0, ind) 

   del split_data, data

   return ready_data

def add_password(url_or_program, user, password):
   password = bytes(password, "utf-8")
   user = bytes(user, "utf-8")
   url_or_program = bytes(url_or_program, "utf-8")
   encrypted_password = (crypto_handler.encryption(key, password)).encode("utf-8")
   encrypted_username = (crypto_handler.encryption(key, user)).encode("utf-8")
   encrypted_url_or_program = (crypto_handler.encryption(key, url_or_program)).encode("utf-8")

   del password, url_or_program, user

   with open("Passwords.encryptx", "ab") as p:
      p.write(base64.b64encode(encrypted_url_or_program) + b"04n$b3e0R5K*" + base64.b64encode(encrypted_username) + b"04n$b3e0R5K*" + base64.b64encode(encrypted_password) + b"\n")            
       
def remove_password(index):
   with open("Passwords.encryptX", "rb") as read:
      lines = read.readlines()
      read.close()
   with open("Passwords.encryptX", "wb") as write:
      for index_of_line, line in enumerate(lines):
         if index_of_line != int(index):
            write.write(line)

   try:
      for item in tree.get_children():
         tree.delete(item)

      ready_data = get_data()
      for line in ready_data:
         tree.insert("", "end", values=(line)) 
      del ready_data
   except:
      pass
      
def password_rating_check(password):
   score = 0
   lowercase_characters_present = uppercase_characters_present = special_characters_present = numbers_present = False

   lowercase_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
   uppercase_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
   special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '|', '\\', ';', ':', "'", '"', ',', '.', '<', '>', '/', '?']
   numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
 
   for char in lowercase_characters:
      if char in password:
         lowercase_characters_present = True
   for char in uppercase_characters:
      if char in password:
         uppercase_characters_present = True
   for char in special_characters:
      if char in password:
         special_characters_present = True
   for char in numbers:
      if char in password:
         numbers_present = True
 
   if lowercase_characters_present == True:
      score +=1

   if uppercase_characters_present == True:
      score +=1

   if special_characters_present == True:
      score +=1

   if numbers_present == True:
      score +=1

   if len(password) >= 8:
      score +=1

   del password

   return score

def password_generator(length: int, special: bool):
   if special == "yes":
      characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*()"
   else:
      characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
   generated_password = ""
   for i in range(length):
      generated_password += random.choice(characters)

   return generated_password

#----------------------------------Main GUI----------------------------------#

def refresh_stats(total_passwords):
   ready_data = get_data()
   global total_passwords_value
   total_passwords_value = len(ready_data)
   total_passwords.configure(text=("Passwords Saved ~> ", total_passwords_value))
   del ready_data

def refresh_treeview(tree):
   for item in tree.get_children():
      tree.delete(item)

   ready_data = get_data()
   for line in ready_data:
      modified_line = list(line)
      modified_line[3] = "••••••••"
      modified_line = tuple(modified_line)
      
      tree.insert("", "end", values=modified_line)

def add_password_gui(root, tree):
   info_window = customtkinter.CTkToplevel(root)
   info_window.geometry("400x200")
   info_window.title("Add Password")
   name_text_box = customtkinter.CTkEntry(info_window, placeholder_text="Name/URL")
   username_text_box = customtkinter.CTkEntry(info_window, placeholder_text="Username")
   password_text_box = customtkinter.CTkEntry(info_window, placeholder_text="Password", show="*")
   name_text_box.pack(padx=10, pady=10)
   username_text_box.pack(padx=10, pady=10)
   password_text_box.pack(padx=10, pady=10)

   def send_info(tree):
      name = name_text_box.get()
      username = username_text_box.get()
      password = password_text_box.get()

      add_password(name, username, password)
      refresh_treeview(tree)

      del password, name, username

      info_window.destroy()

   save_button = tkinter.Button(info_window, text="Add Password", command=lambda: send_info(tree))
   save_button.pack(pady=5)

def copy_user_or_pass(itemid, copy):
   ready_data = get_data()
   data = ready_data[int(itemid)]

   if copy == "user":
      user = data[2]
      pyperclip.copy(user)
      del user, ready_data
   elif copy == "pass":
      password = data[3]
      pyperclip.copy(password)
      del password, ready_data
   else:
      pass

def show_password(tree, item):
   ready_data = get_data()
   data = ready_data[int(item)]

   for item in tree.get_children():
      tree.delete(item)

   for line in ready_data:
      if line == data:
         tree.insert("", "end", values=line)
      else:
         modified_line = list(line)
         modified_line[3] = "••••••••"
         modified_line = tuple(modified_line)

         tree.insert("", "end", values=modified_line)
      
   del data, modified_line, line, ready_data

def autotype(items: list):
    DELAY = 0.05
    windows = list(filter(None, gw.getAllTitles()))
    msg = CTkMessagebox(title="Autotype", message=f"Auto Type In Previous Window?",
                        icon="question", option_1="No", option_2="Yes", width=300, height=100)
    response = msg.get()
    if response=="Yes":
        win = gw.getWindowsWithTitle(windows[1])[0]
        win.activate()
        time.sleep(2)
        if len(items) > 1:
            for index, item in enumerate(items):
                if index == len(items):
                    return
                else:
                    pyautogui.typewrite(item, interval=DELAY)
                    keyboard.press("tab")
        else:
            pyautogui.typewrite(items[0], interval=DELAY)
    else:
        return

def on_right_click(event):
   item = tree.identify_row(event.y)
   if item != "":
      item_id = tree.item(item, "values")[0]

   if item:
      menu = tkinter.Menu(root, tearoff=0)
      autotype_menu = tkinter.Menu(menu, tearoff=0)
      menu.add_command(label="Remove Item", command=lambda:remove_password(item_id))
      menu.add_command(label="Copy Username", command=lambda:copy_user_or_pass(item_id, copy="user"))
      menu.add_command(label="Copy Password", command=lambda:copy_user_or_pass(item_id, copy="pass"))
      menu.add_command(label="Show Password", command=lambda:show_password(tree, item_id))
      menu.add_command(label="Hide Password", command=lambda:refresh_treeview(tree))

      autotype_menu.add_command(label="USERNAME & PASSWORD -> {USERNAME}{TAB}{PASSWORD}", command=lambda: autotype([get_data()[int(item_id)][2], get_data()[int(item_id)][3]]))
      autotype_menu.add_command(label="USERNAME -> {USERNAME}", command=lambda: autotype([get_data()[int(item_id)][2]]))
      autotype_menu.add_command(label="PASSWORD -> {PASSWORD}", command=lambda: autotype([get_data()[int(item_id)][3]]))
      

      menu.add_cascade(label="Auto Type", menu=autotype_menu)
      menu.tk_popup(event.x_root, event.y_root)

def combobox_callback(choice):
   if choice == "Dark Mode":
      customtkinter.set_appearance_mode("dark")
   elif choice == "Light Mode":
      customtkinter.set_appearance_mode("light")
   else:
      pass

def combobox_callback(choice):
   if choice == "Dark Mode":
      customtkinter.set_appearance_mode("dark")
   elif choice == "Light Mode":
      customtkinter.set_appearance_mode("light")
   else:
      pass

def slider_event(value):
   global password_generated
   special = use_special.get()
   password_generated = password_generator(int(value), special)
   length_set.configure(text=f"Password Length: {int(value)}")
   password_generated_label.configure(text=f"Password: {password_generated}")
   
def checkbox_event():
   global length, password_generated
   length = slider.get()
   special = use_special.get()
   password_generated = password_generator(int(length), special)
   password_generated_label.configure(text=f"Password: {password_generated}")

def main_gui():
   global root, tree

   keyboard.add_hotkey('Ctrl+Alt+L', lock_bind)

   root = customtkinter.CTk()
   root.geometry("1400x800")
   root.title(f"EncryptX {version}")

   tabview = customtkinter.CTkTabview(root, width=1400, height=800)
   tabview.pack(pady=5,padx=5)
   tabview.add("Passwords")
   tabview.add("Password Generator") 
   tabview.add("Binds")
   tabview.add("Stats")
   tabview.add("Settings") 

   # Password Page   

   try: 
      ready_data = get_data()
   except:
      pass  

   style = tkinter.ttk.Style(root)
   style.theme_use("clam")
   style.configure("Treeview", background="#565656", fieldbackground="#060202", foreground="white")
   tree = tkinter.ttk.Treeview(master=tabview.tab("Passwords"), columns=("ID", "Name/URL", "Username", "Password", "Password_Rating"), show="headings", style="Treeview")

   scrollbar = tkinter.ttk.Scrollbar(tree, orient=tkinter.VERTICAL, command=tree.yview)
   tree.configure(yscroll=scrollbar.set) 

   tree.heading("ID", text="ID")
   tree.heading("Name/URL", text="Name/URL")
   tree.heading("Username", text="Username")
   tree.heading("Password", text="Password")
   tree.heading("Password_Rating", text="Password Rating (1-5)")  

   refresh_treeview(tree)

   tree.column("ID", anchor="center")
   tree.column("Name/URL", anchor="center")
   tree.column("Username", anchor="center")
   tree.column("Password", anchor="center")
   tree.column("Password_Rating", anchor="center") 

   tree.pack(fill="both", expand=True) 

   tree.bind("<Button-3>", on_right_click)

   add_password_button = customtkinter.CTkButton(master=tabview.tab("Passwords"), text="Add Password", font=("Cascadia Code", 12), command=lambda: add_password_gui(root, tree))
   add_password_button.pack(pady=(10,5), padx=5)

   refresh_button = customtkinter.CTkButton(master=tabview.tab("Passwords"), text="Refresh Passwords List", font=("Cascadia Code", 12), command=lambda: refresh_treeview(tree))
   refresh_button.pack() 

   # Password Generator

   length = 1

   global password_generated_label
   password_generated_label = customtkinter.CTkLabel(master=tabview.tab("Password Generator"), text=f"Password: Select A Length", font=("Cascadia Code", 16))
   password_generated_label.pack(pady=(20,5), padx=5)

   global length_set
   length_set = customtkinter.CTkLabel(master=tabview.tab("Password Generator"), text=f"Password Length: {int(length)}", font=("Cascadia Code", 16))
   length_set.pack(pady=(20,5), padx=5)

   global slider
   slider = customtkinter.CTkSlider(master=tabview.tab("Password Generator"), from_=1, to=44, command=slider_event)
   slider.pack(pady=(10,5), padx=5)
   slider.configure(number_of_steps=49)
   slider.set(1)

   global use_special
   use_special = customtkinter.CTkCheckBox(master=tabview.tab("Password Generator"), text="Special Characters", onvalue="yes", offvalue="no", command=checkbox_event)
   use_special.pack(pady=(10,5), padx=5)

   copy_password_button = customtkinter.CTkButton(master=tabview.tab("Password Generator"), text="Copy Password", font=("Cascadia Code", 18), command=lambda: pyperclip.copy(password_generated))
   copy_password_button.pack(pady=(10,5), padx=5)

   # Binds

   title_binds = customtkinter.CTkLabel(master=tabview.tab("Binds"), text="EncryptX Binds", font=("Cascadia Code", 22))
   title_binds.pack(pady=15, padx=10)

   exit_bind_label = customtkinter.CTkLabel(master=tabview.tab("Binds"), text="Exit >> Ctrl+Alt+E", font=("Cascadia Code", 12))
   exit_bind_label.pack(pady=(10,5), padx=5)

   lock_bind_label = customtkinter.CTkLabel(master=tabview.tab("Binds"), text="Lock >> Ctrl+Alt+L", font=("Cascadia Code", 12))
   lock_bind_label.pack(pady=(10,5), padx=5)

   # Stats Page

   title_stats = customtkinter.CTkLabel(master=tabview.tab("Stats"), text="EncryptX Stats", font=("Cascadia Code", 22))
   title_stats.pack(pady=15, padx=10)

   total_passwords_value = len(ready_data)
   total_passwords_label = customtkinter.CTkLabel(master=tabview.tab("Stats"), text=("Passwords Saved ~> ", total_passwords_value), font=("Cascadia Code", 12))
   total_passwords_label.pack(pady=(10,5), padx=5)

   refresh_button_stats = customtkinter.CTkButton(master=tabview.tab("Stats"), text="Refresh Stats", font=("Cascadia Code", 12), command=lambda: refresh_stats(total_passwords_label))
   refresh_button_stats.pack() 

   # Settings Page

   combobox_var = customtkinter.StringVar(value="Dark Mode")
   combobox = customtkinter.CTkComboBox(master=tabview.tab("Settings"), values=["Dark Mode", "Light Mode"], font=("Cascadia Code", 16) ,command=combobox_callback, variable=combobox_var)
   combobox_var.set("Dark Mode")
   combobox.pack(pady=(10,5), padx=5)

   root.mainloop()  

#----------------------------------Login Functions----------------------------------#

def login_check(master_pass):
   global key

   key = crypto_handler.generate_key(master_pass)

   with open("UserData.encryptx", "r") as r:
      userdata = r.read()
      r.close()

   decrypted_password = crypto_handler.decryption(key, userdata)
   if decrypted_password != None:
      if decrypted_password.decode("utf-8") == master_pass:
         login.destroy()
         del master_pass, decrypted_password
         main_gui()
      else:
         login.destroy()
         exit()

   login.destroy()
   exit()
             
def login_create(master_pass, second_entry):
   global key

   if master_pass != second_entry:
      login.destroy()
      exit()

   key = crypto_handler.generate_key(master_pass)
   encoded_password = bytes(master_pass, "utf-8")
   encrypted_password = crypto_handler.encryption(key, encoded_password)

   with open("UserData.encryptx", "w") as w:
      w.write(encrypted_password)
      w.close()

   del master_pass

   login.destroy()
   main_gui()

def login_creation_gui():
   global login

   hwnd = ctypes.windll.kernel32.GetConsoleWindow()
   if hwnd:
      ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)

   login = customtkinter.CTk()
   login.geometry("400x300")
   login.resizable(width=0, height=0)
   login.title(f"EncryptX {version} ~ Account Creation")

   title = customtkinter.CTkLabel(master=login, text="EncryptX", font=("Cascadia Code", 32))
   title.pack(pady=20, padx=5)

   password_box = customtkinter.CTkEntry(master=login, placeholder_text="Password", font=("Cascadia Code", 14), show="*")
   second_password_box = customtkinter.CTkEntry(master=login, placeholder_text="Re-Enter Password", font=("Cascadia Code", 14), show="*")
   password_box.pack(pady=5, padx=5)
   second_password_box.pack(pady=5, padx=5)

   button = customtkinter.CTkButton(master=login, text="Create Account", font=("Cascadia Code", 14), command=lambda:login_create(password_box.get(), second_password_box.get()))
   button.pack(pady=20, padx=5)

   login.mainloop()

def login_gui():
   global login

   hwnd = ctypes.windll.kernel32.GetConsoleWindow()
   if hwnd:
      ctypes.windll.user32.ShowWindow(hwnd, SW_HIDE)

   login = customtkinter.CTk()
   login.geometry("400x300")
   login.resizable(width=0, height=0)
   login.title(f"EncryptX {version} ~ Account Login")

   title = customtkinter.CTkLabel(master=login, text="EncryptX", font=("Cascadia Code", 22))
   title.pack(pady=20, padx=5)

   password_box = customtkinter.CTkEntry(master=login, placeholder_text="Password", font=("Cascadia Code", 14), show="*")
   password_box.pack(pady=5, padx=5)

   button = customtkinter.CTkButton(master=login, text="Login", font=("Cascadia Code", 14), command=lambda:login_check(password_box.get()))
   button.pack(pady=20, padx=5)

   login.mainloop()

#----------------------------------Boot----------------------------------#

def boot():
   global crypto_handler

   keyboard.add_hotkey('Ctrl+Alt+E', exit_bind)

   crypto_handler = CryptoHandler()

   customtkinter.set_appearance_mode("dark")

   if os.path.exists("UserData.encryptx"):
      new_user = False
   else:
      new_user = True

   if new_user == True:
      login_creation_gui()
   elif new_user == False:
      login_gui()

if __name__=="__main__":
   boot()
