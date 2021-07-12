#!/opt/homebrew/bin/python3

import json, os, getpass

from art import text2art

from boyer import clear

items = ["username", "password", "URL"]
lock = False
wiped = False

if os.path.exists('storage/.data.json'):
    with open('storage/.data.json', 'r') as file:
        data = json.load(file)
else:
    data = {
        "passwords": 0,
        "unlocks": 0,
        "commands": 0,
        "security-incidents": 0
    }
if data == {}:
    data = {
        "passwords": 0,
        "unlocks": 0,
        "commands": 0,
        "security-incidents": 0
    }    

def save_data(data):
    with open('storage/.data.json', 'w') as file:
        json.dump(data, file, indent=4)

save_data(data)

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
                break
            else:
                print("Wrong username!")
                continue
        incorrect = 0
        while True:
            entered_password = getpass.getpass("Password: ")
            if entered_password == credentials["password"]:
                data['unlocks'] += 1
                save_data(data)
                break
            else:
                print("Incorrect password!")
                incorrect += 1
                if incorrect == 5:
                    print("Too many incorrect passwords!")
                    lock = True
                    data["security-incidents"] += 1
                    save_data(data)
                    break
                continue
    
else:
    credentials = {}
    print("Welcome to Boyer's password generator!\nLet's get you started with some credentials\n")
    credentials["username"] = input("Create a username: ")
    while True:
        user_pass = getpass.getpass("Create a password: ")
        if user_pass == getpass.getpass("Confirm password: "):
            print("Password confirmed!")
            data['unlocks'] += 1
            save_data(data)
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
    with open('storage/.passwords.json', 'w') as file:
        json.dump(passwords, file, indent=4)

username = credentials['username']

commands = """
"quit": to quit the program
"man": to display this message again
"clear": to clear the terminal window
"new": to create a new password
"save": to save your passwords to file
"wipe": to delete all data stored in the password manager
"edit": edit a password
"get": display a password
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
        edit()
    elif cmd == "":
        list()
    else:
        print('not a command')
        local_errors = errors + 1
        if local_errors == 3 or local_errors == 5 or local_errors > 10:
            print("use 'man' to display help message")
    if cmd != "quit" or local_errors != 0:
        data['commands'] += 1
        save_data(data)
    return local_errors


def save():
    with open("storage/.passwords.json", "w") as file:
        json.dump(passwords, file, indent=4)
    with open("storage/.config.json", "w") as file:
        json.dump(credentials, file, indent=4)
    with open('storage/.data.json', 'w') as file:
        json.dump(data, file, indent=4)

def quit():
    save()
    raise terminate

def list():
    print("\nAll your passwords:")
    for key in passwords.keys():
        print(f"~ {key}")
    print("")

def man():
    # print("Welcome to Andrew Boyer's password manager!\nHere are all available commands:")
    print(commands)

def clean(text):
    return text.lower().strip()

def get_pass():
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
            return 0
        else:
            print("Not a password. Press enter to list all of your passwords.")
    print(passwords[password])
    print()

def new():

    while True:
        
        name = input("Password name: ").strip()

        if name == '':
            print("Please enter a valid password name!") 
        
        elif name == "QUIT":
            return 0

        elif name in passwords.keys():
            print("Please enter a unique password name!")
        
        else:
            break   

    passwords[name] = {}

    for item in items:
        user_input = input(f"{item[0].upper() + item[1:]} for {name}: ").strip()
        if user_input == "QUIT":
            return 0
        elif user_input.strip() == "" and item == "URL":
            passwords[name][item] = f'https://{name.lower().strip()}.com'
        else:
            passwords[name][item] = user_input

    save()

def edit():
    while True:
        password = input("Which password would you like to edit? ")
        if password in passwords.keys():
            break
        elif password.strip() == "":
            print("\nAll your passwords:")
            for key in passwords.keys():
                print(f"~ {key}")
                print("")
        elif password == 'QUIT':
            return 0
        else:
            print(f"You don't have a password named {password.strip()}!")
            continue
    while True: 
        item = input('What item would you like to edit? ')
        if item in items:
            break
        elif item == 'name':
            print(f'Previous name: {password}')
            passwords[input(f'New name for {password}: ')] = passwords[password]
            del passwords[password]
            save()
            return 0
        else:
            print('Not a valid field!')
            continue
    print(f'Previous {item} for {password}: {passwords[password][item]}')
    passwords[password][item] = input(f'New {item} for {password}: ')
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
            return 0
        else:
            print("Enter a y or n")
            continue
    entered_password = getpass.getpass("Please confirm your password: ")
    passwords, credentials, data = read_data()
    if entered_password == credentials["password"]:
        print("Wiping all data...")
        pass
    else:
        print("Incorrect password... terminating program!\n\n[this incident will be reported]")
        wipe = False
        data["security-incidents"] += 1
        save_data(data)
    if wipe:
        passwords = {}
        credentials = {}
        data = {
            "passwords": 0,
            "unlocks": 0,
            "commands": 0,
            "security-incidents": 0
        }
        with open("storage/.passwords.json", "w") as file:
            json.dump(passwords, file, indent=4)
        with open("storage/.config.json", "w") as file:
            json.dump(credentials, file, indent=4)
        with open("storage/.data.json", "w") as file:
            json.dump(data, file, indent=4)
        print("All data wiped!")

def read_data():
    with open("storage/.config.json", "r") as file:
        credentials  = json.load(file)
    with open("storage/.passwords.json", "r") as file:
        passwords = json.load(file)
    with open("storage/.data.json", "r") as file:
        data = json.load(file)
    return passwords, credentials, data

if data["unlocks"] < 1:
    start()
elif not lock:
    clear()

while not lock:
    try:
        data["passwords"] = 0
        for password in passwords:
            data["passwords"] += 1
            save_data(data)
        cmd = input(f"{username}$ ")
        passwords, credentials, data = read_data()
        # print(data)          
        errors = user_cmd(cmd)
    except terminate:
        break

# Written by Andrew Boyer
# https://asboyer.com
