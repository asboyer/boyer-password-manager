#!/opt/homebrew/bin/python3

import json, os, getpass

from art import text2art

from boyer import clear

clear()

class terminate(Exception): pass
errors = 0

if os.path.exists("storage/.config.json"):
    with open("storage/.config.json", "r") as file:
        credentials  = json.load(file)
    if credentials == {}:
        print("Welcome to Boyer's password generator!\nLet's get you started with some credentials\n")
        credentials["username"] = input("Create a username: ")
        while True:
            user_pass = getpass.getpass("Create a password: ")
            if user_pass == getpass.getpass("Confirm password: "):
                print("Password confirmed!")
                credentials["password"] = user_pass
                with open("storage/.config.json", "w") as file:
                    json.dump(credentials, file, indent=4)
                break
            else:
                print("Passwords do not match!")
    else:
        while True:
            entered_username = input("Username: ")
            if entered_username == credentials["username"]:
                pass
            else:
                print("Wrong username!")
                continue
            
            entered_password = getpass.getpass("Password: ")
            if entered_password == credentials["password"]:
                print(f"Welcome {credentials['username']}")
                break
            else:
                print("Incorrect password!")
    
else:
    credentials = {}
    print("Welcome to Boyer's password generator!\nLet's get you started with some credentials\n")
    credentials["username"] = input("Create a username: ")
    while True:
        user_pass = getpass.getpass("Create a password: ")
        if user_pass == getpass.getpass("Confirm password: "):
            print("Password confirmed!")
            credentials["password"] = user_pass
            with open("storage/.config.json", "w") as file:
                json.dump(credentials, file, indent=4)
            break
        else:
            print("Passwords do not match!")

with open("storage/.config.json", "r") as file:
    credentials  = json.load(file)

if os.path.exists("storage/.passwords.json"):
    with open("storage/.passwords.json", "r") as file:
        passwords = json.load(file)
else:
    passwords = {}

username = credentials['username']

commands = """
"quit": to quit the program
"man": to display this message again
"clear": to clear the terminal window
"new": to create a new password
"save": to save your passwords to file
"""

def user_cmd(cmd):
    local_errors = 0
    cmd_raw = cmd
    cmd = clean(cmd)
    if cmd == "quit":
        quit()
    elif cmd == 'man' or cmd == 'help':
        man()
    elif cmd == 'cls' or cmd == 'clear':
        clear()
    elif cmd == 'new':
        new()
    elif cmd == 'save':
        save()
    elif cmd == 'get':
        get_pass()
    elif cmd == 'wipe':
        wipe()
    elif cmd == 'edit':

    else:
        print('not a command')
        local_errors = errors + 1
        if local_errors == 3 or local_errors == 5 or local_errors > 10:
            print("use 'man' to display help message")
    return local_errors


def save():
    with open("storage/.passwords.json", "w") as file:
        json.dump(passwords, file, indent=4)
    with open("storage/.config.json", "w") as file:
        json.dump(credentials, file, indent=4)

def quit():
    save()
    raise terminate

def edit():
    quit = False
    while True:
        password = input("Which password would you like to edit? ")
        if password in passwords.keys():
            pass
        elif password == 'QUIT':
            quit = True
            break
        else:
            print()

def man():
    print("Welcome to Andrew Boyer's password manager!\nHere are all available commands:\n")
    print(commands)

def clean(text):
    return text.lower().strip()

def get_pass():
    quit = False
    while True:
        password = input("Which password? ").strip()
        if password == "":
            print("\nAll your passwords:")
            for key in passwords.keys():
                print(f"~ {key}")
            print("")
        elif password in passwords.keys():
            break
        elif password == "QUIT":
            quit = True
            break
        else:
            print("Not a password. Press enter to list all of your passwords.")
    if not quit:
        print(passwords[password])
        print()

def new():
    while True:
        
        name = input("Password name: ").strip()

        if name == '':
            print(passwords.keys())
            print("Please enter a valid password name!") 
        
        elif name in passwords.keys():
            print("Please enter a unique password name!")
        
        else:
            break   


    passwords[name] = {}

    username = input(f"Username for {name}: ").strip()
    passwords[name]["username"] = username

    password = input(f"Password for {name}: ").strip()
    passwords[name]["password"] = password

    url = input(f"URL for {name}: ").strip()
    passwords[name]["URL"] = url

    save()

def start():
    clear()
    print(text2art("Boyer's\nPassword\nManager!"))
    input("\nPress enter to start")
    clear()

def wipe():
    wipe = True
    while True:
        answer = input("Are you sure you want to wipe all passwords? (y/n) ").lower().strip()
        if answer.startswith("y"):
            break
        elif answer.startswith("n"):
            wipe = False
            break
        else:
            print("Enter a y or n")
            continue
    if wipe:
        passwords = {}
        credentials = {}
        with open("storage/.passwords.json", "w") as file:
            json.dump(passwords, file, indent=4)
        with open("storage/.config.json", "w") as file:
            json.dump(credentials, file, indent=4)

def read_data():
    with open("storage/.config.json", "r") as file:
        credentials  = json.load(file)
    with open("storage/.passwords.json", "r") as file:
        passwords = json.load(file)
    return passwords, credentials

start()

while True:
    try:
        cmd = input(f"{username}$ ")
        passwords, credentials = read_data()
        errors = user_cmd(cmd)
    except terminate:
        break

# Written by Andrew Boyer
# https://asboyer.com
