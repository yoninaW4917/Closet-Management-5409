#-----------------------------------------------------------------------------
# Name:        closetman.py
# Purpose:     This inventory tool is designed for electrical members and anyone that wants to organize their closets with a simple, easy to understand UI where you can inventory drawers easily!
#
# Author:      Yonina Wu
# Created:     2024.05.08
# Updated:     2024.06.04
#-----------------------------------------------------------------------------
# I think this project deserves a level 4+ because I used various libraries, including PySimpleGUI, TiyDB, cryptography and Pygame, 
# showing my understanding of different modules. I read through the documentations and researched to implemented all the listed features, 
# This project demonstrated my learning and application of advanced Python concepts, showing the high-level problem solving skills I
# developed throughout this course :)
#
# Features Added:
#   Data Encryption: Utilized the cryptography library's Fernet module to encrypt and decrypt data
#   File Reading and Writing: Implemented functionality to read from and write to JSON files, storing data in a structured format using the TinyDB library
#   Integration with PyGame: Incorporated a PyGame-based mini-game ("catch.py") 
#       including data storage, sound effects, and image handling
#   UI Design: User-friendly GUI with PySimpleGUI
#   Data Validation: Added input validation to ensure data integrity, ie. verifying numeric input for item quantities 
#   
#-----------------------------------------------------------------------------
import os
import PySimpleGUI as sg
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from cryptography.fernet import Fernet
import base64
import hashlib
import json
import subprocess

# Constants
imageFileName = "chargers.jpg"
dataFolder = "data"

# Theme
sg.theme('DarkGrey2')

def generateKey(password):
    """
    Generate an encryption key from a password.

    Args:
        password (str): The password to generate the key from.

    Returns:
        bytes: The generated encryption key.
    """
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encryptData(data, key):
    """
    Encrypt data using the provided key.

    Args:
        data (str): The data to encrypt.
        key (bytes): The encryption key.

    Returns:
        str: The encrypted data as a string.
    """
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decryptData(data, key):
    """
    Decrypt data using the provided key.

    Args:
        data (str): The encrypted data to decrypt.
        key (bytes): The encryption key.

    Returns:
        str: The decrypted data as a string.
    """
    fernet = Fernet(key)
    return fernet.decrypt(data.encode()).decode()

def loadData(username, password):
    """
    Load data from a file, decrypt it, and load it into a TinyDB instance.

    Args:
        username (str): The username to determine the file name.
        password (str): The password to decrypt the data.

    Returns:
        Tuple[TinyDB, Table]: The TinyDB instance and the drawers table.
    """
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
        
    filePath = os.path.join(dataFolder, f"{username}.json")
    
    if os.path.exists(filePath):
        with open(filePath, 'r') as file:
            encryptedData = file.read()
        try:
            decryptedData = decryptData(encryptedData, generateKey(password))
            db = TinyDB(storage=MemoryStorage)  # type: ignore
            db.storage.write(json.loads(decryptedData))  # Load decrypted data into TinyDB
            drawersTable = db.table('drawers')
            return db, drawersTable
        except Exception as e:
            sg.popup_error("Invalid password or data corrupted!", str(e))
            return None, None
    else:
        db = TinyDB(filePath)
        drawersTable = db.table('drawers')
        return db, drawersTable

def saveData(username, password, db):
    """
    Save data from a TinyDB instance to a file, encrypting it.

    Args:
        username (str): The username to determine the file name.
        password (str): The password to encrypt the data.
        db (TinyDB): The TinyDB instance containing the data.
    """
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
    
    filePath = os.path.join(dataFolder, f"{username}.json")
    data = json.dumps(db.storage.read())  # Serialize the data from TinyDB
    encryptedData = encryptData(data, generateKey(password))
    with open(filePath, 'w') as file:
        file.write(encryptedData)

def readData():
    """
    Read and return all data from the drawers table.

    Returns:
        dict: The data from the drawers table.
    """
    data = {}
    for item in drawersTable.all():
        data[item['drawer']] = item['items']
    return data

def writeData(data):
    """
    Write data to the drawers table.

    Args:
        data (dict): The data to write to the drawers table.
    """
    drawersTable.truncate()  # Clear the table first
    for key, items in data.items():
        drawersTable.insert({'drawer': key, 'items': items})

def popup(title, message):
    """
    Create a popup window with a message.

    Args:
        title (str): The title of the popup window.
        message (str): The message to display in the popup window.
    """
    layout = [
        [sg.Text(message)],
        [sg.Button('OK')]
    ]
    window = sg.Window(title, layout, modal=True)
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED or event == 'OK':
            break
    window.close()

# Get username and password
username = sg.popup_get_text("Enter your username:")
if username is None:  # If the user cancels, exit the program
    exit()

password = sg.popup_get_text("Enter your password:", password_char='*')
if password is None:  # If the user cancels, exit the program
    exit()

# Initialize the database
db, drawersTable = loadData(username, password)
if db is None:
    exit()

# Main GUI layout
layout = [
    [sg.Text("Choose an option:")],
    [sg.Button("New Drawer"), sg.Button("Add/Remove Item"), sg.Button("Search for Item"), sg.Button("Display Drawer")],
    [sg.Button("Remove Drawer")], 
    [sg.Button("Tired?")],  # New Button
    [sg.Exit()]
]

# Create the window
window = sg.Window("Drawer Management System", layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        saveData(username, password, db)
        break
    
    data = readData()

    if event == "New Drawer":
        drawerName = sg.popup_get_text("Enter the drawer name:")
        if drawerName:
            if drawerName in data:
                if sg.popup_yes_no(f"Drawer '{drawerName}' already exists. Do you want to overwrite it?") == 'No':
                    continue
            objectName = sg.popup_get_text("Enter the first object name for the drawer:")
            if objectName:
                quantity = sg.popup_get_text("Enter the quantity for the item:")
                if quantity and quantity.isdigit():
                    data[drawerName] = [{'name': objectName, 'quantity': int(quantity)}]
                    while sg.popup_yes_no("Do you want to add another object?") == 'Yes':
                        objectName = sg.popup_get_text("Enter the next object name:")
                        if objectName:
                            quantity = sg.popup_get_text("Enter the quantity for the item:")
                            if quantity and quantity.isdigit():
                                data[drawerName].append({'name': objectName, 'quantity': int(quantity)})
                            else:
                                popup("Error", "Quantity must be a number!")
                                break
                    writeData(data)
                    popup("Success", "Drawer and objects added successfully!")
                else:
                    popup("Error", "Quantity must be a number!")

    elif event == "Add/Remove Item":
        drawerName = sg.popup_get_text("Enter the drawer name:")
        if drawerName in data:
            action = sg.popup_get_text("Enter 'a' to add an item or 'r' to remove an item:")
            if action == 'a':
                objectName = sg.popup_get_text("Enter the object name to add:")
                if objectName:
                    quantity = sg.popup_get_text("Enter the quantity for the item:")
                    if quantity and quantity.isdigit():
                        data[drawerName].append({'name': objectName, 'quantity': int(quantity)})
                        writeData(data)
                        popup("Success", f"Object '{objectName}' added to drawer '{drawerName}'!")
                    else:
                        popup("Error", "Quantity must be a number!")
            elif action == 'r':
                objectName = sg.popup_get_text("Enter the object name to remove:")
                found = False
                for item in data[drawerName]:
                    if item['name'] == objectName:
                        data[drawerName].remove(item)
                        found = True
                        writeData(data)
                        popup("Success", f"Object '{objectName}' removed from drawer '{drawerName}'!")
                        break
                if not found:
                    popup("Error", f"Object '{objectName}' not found in drawer '{drawerName}'")
            else: 
                popup("Error", "Please enter 'a' or 'r' for add or remove!")
        else:
            popup("Error", f"Drawer '{drawerName}' not found")

    elif event == "Search for Item":
        searchItem = sg.popup_get_text("Enter the object name to search for:")
        foundItems = []
        for drawer, items in data.items():
            for item in items:
                if item['name'] == searchItem:
                    foundItems.append(f"{item['name']} (Quantity: {item['quantity']}) found in drawer '{drawer}'")
        if foundItems:
            popup("Found", "\n".join(foundItems))
        else:
            popup("Not Found", f"Object '{searchItem}' not found")

    elif event == "Display Drawer":
        drawerNames = list(data.keys())
        if drawerNames:
            layout = [
                [sg.Text('Select a drawer to display:')],
                [sg.Combo(drawerNames, key='-DRAWER-', readonly=True)],
                [sg.Button('OK'), sg.Button('Cancel')]
            ]
            windowSelect = sg.Window("Select Drawer", layout)
            eventSelect, valuesSelect = windowSelect.read()
            if eventSelect == 'OK' and valuesSelect['-DRAWER-']:
                drawerName = valuesSelect['-DRAWER-']
                if drawerName in data:
                    itemsList = "\n".join([f"{item['name']} (Quantity: {item['quantity']})" for item in data[drawerName]])
                    popup("Drawer Contents", f"Drawer '{drawerName}' contains:\n{itemsList}")
                else:
                    popup("Error", f"Drawer '{drawerName}' not found")
            windowSelect.close()
        else:
            popup("Error", "No drawers available to display")

    elif event == "Remove Drawer":
        drawerNames = list(data.keys())
        if drawerNames:
            layout = [
                [sg.Text('Select a drawer to remove:')],
                [sg.Combo(drawerNames, key='-DRAWER-', readonly=True)],
                [sg.Button('OK'), sg.Button('Cancel')]
            ]
            windowRemove = sg.Window("Select Drawer to Remove", layout)
            eventRemove, valuesRemove = windowRemove.read()
            if eventRemove == 'OK' and valuesRemove['-DRAWER-']:
                drawerName = valuesRemove['-DRAWER-']
                if drawerName in data:
                    itemsList = "\n".join([f"{item['name']} (Quantity: {item['quantity']})" for item in data[drawerName]])
                    if sg.popup_yes_no(f"Are you sure you want to remove drawer '{drawerName}'? It contains:\n{itemsList}") == 'Yes':
                        del data[drawerName]
                        writeData(data)
                        popup("Success", f"Drawer '{drawerName}' removed successfully!")
                else:
                    popup("Error", f"Drawer '{drawerName}' not found")
            windowRemove.close()
        else:
            popup("Error", "No drawers available to remove")

    elif event == "Tired?":
        subprocess.Popen(["python", "catch.py"])  # This line runs catch.py

window.close()
