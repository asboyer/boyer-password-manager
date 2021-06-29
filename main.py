#!/opt/homebrew/bin/python3

import json, os, getpass

# from art import text2art

# from boyer import clear

class terminate(Exception): pass
errors = 0

if os.path.exists("storage/passwords.json"):
    with open("storage/passwords.json", "r") as file:
        passwords = json.load(file)
else:
    passwords = {}

need_pass = False
quit = False

if os.path.exists("storage/.config.json"):
	with open("storage/.config.json", "r") as file:
		credentials  = json.load(file)
	if credentials == {}:
		need_pass = True
	else:
        while True:
		entered_username = getpass.getpass("Username: ")
		if entered_username == credentials["username"]:
			pass
		else:
			print("Wrong username!")
		
		if not quit:
			entered_password = getpass.getpass("Password: ")
			if entered_password == credentials["password"]:
				print(f"Welcome {credentials["username"]}")
			else:
				print("Incorrect username!")
		
else or need_pass:
	credentials = {}
	print("Welcome to Boyer's password generator!\nLet's get you started with some credentials")
	credentials["username"] = input("Create a username: ")
	while True:
		user_pass = getpass.getpass("Create a password: ")
		if user_pass == getpass.getpass("Confirm password: "):
			print("Password confirmed!")
			credentials["password"] = user_pass
		else:
			print("Passwords do not match!")

commands = """
"quit": to quit the program
"man": to display this message again
"clear": to clear the terminal window
"new": to create a new password
"save": to save your passwords to file
"""

def clear():
    os.system('clear')

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
        while True:
            answer = input("Are you sure you want to wipe all passwords? (y/n) ").lower().strip()
            if answer.startswith("y"):
                passwords = {}
                break
            elif answer.startswith("n"):
                break
            else:
                print("Enter a y or n")

        passwords = {}
    else:
        print('not a command')
        local_errors = errors + 1
        if local_errors == 3 or local_errors == 5 or local_errors > 10:
            print("use 'man' to display help message")
    return local_errors


def save():
    with open("storage/passwords.json", "w") as file:
        json.dump(passwords, file, indent=4)
	with open("storage/.config.json", "w") as file:
		json.dump(credentials, file, indent=4)

def quit():
    save()
    raise terminate

def man():
    print("Welcome to Andrew Boyer's password manager!\nHere are all available commands:\n")
    print(commands)

def clean(text):
    return text.lower().strip()

def get_pass():
    while True:
        password = input("Which password? ")
        if password == "show":
            print("\nAll your passwords:")
            for key in passwords.keys():
                print(f"~ {key}")
            print("")
        else:
            break
    print(passwords[password])
    print("\n")

def new():
    while True:
        
        name = input("Password name: ")

        if name == '':
            print(passwords.keys())
            print("Please enter a valid password name!") 
        
        elif name in passwords.keys():
            print("Please enter a unique password name!")
        
        else:
            break   


    passwords[name] = {}

    username = input(f"Username for {name}: ")
    passwords[name]["username"] = username

    password = input(f"Password for {name}: ")
    passwords[name]["password"] = password

    url = input(f"URL for {name}: ")
    passwords[name]["URL"] = url

    save()

def start():
    clear()
    # print(text2art("Boyer's\nPassword\nManager!"))
    print("welcome to boyer's password manager!".upper())
   	input("\nPress enter to start")
    clear()

start()

while True:
    try:
        cmd = input(f"{getpass.getuser()}$ ")
        errors = user_cmd(cmd)
    except terminate:
        break
