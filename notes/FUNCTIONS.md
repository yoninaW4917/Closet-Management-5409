
# Program

```python
import os
import PySimpleGUI as sg
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from cryptography.fernet import Fernet
import base64
import hashlib
import json
import subprocess
```
These import statements bring in the necessary libraries for the application:
- `os` is used for interacting with the operating system, such as checking if directories or files exist.
- `PySimpleGUI` is used for creating the graphical user interface (GUI).
- `TinyDB` is a lightweight document-oriented database used for storing drawer data.
- `MemoryStorage` allows TinyDB to use in-memory storage.
- `Fernet` from the `cryptography` library is used for encryption and decryption.
- `base64` and `hashlib` are used for encoding and generating the encryption key.
- `json` is used for handling JSON data serialization.
- `subprocess` is used to run external scripts or programs.

```python
# Constants
imageFileName = "chargers.jpg"
dataFolder = "data"
```
These constants are defined for the image file name (though it's not used in the current code) and the folder where data will be stored.

```python
# Theme
sg.theme('DarkGrey2')
```
Sets the theme for the PySimpleGUI window.

### Function: `loadData`

```python
def loadData(username, password):
    """
    Load data from a file, decrypt it, and load it into a TinyDB instance.

    Args:
        username (str): The username to determine the file name.
        password (str): The password to decrypt the data.

    Returns:
        Tuple[TinyDB, Table]: The TinyDB instance and the drawers table.
    """
```
- This function loads encrypted data from a file, decrypts it using the given password, and loads it into a TinyDB instance.
- It returns the TinyDB instance and the specific table within the database (`drawers`).

```python
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
```
- Checks if the directory for storing data files (`dataFolder`) exists. If it doesn't, it creates the directory.

```python
    filePath = os.path.join(dataFolder, f"{username}.json")
```
- Constructs the file path for the user's data file using the username. The file will be named `<username>.json` and located in the `dataFolder`.

```python
    if os.path.exists(filePath):
        with open(filePath, 'r') as file:
            encryptedData = file.read()
```
- Checks if the data file for the user exists. If it does, it opens the file in read mode and reads the encrypted data into the variable `encryptedData`.

```python
        try:
            decryptedData = decryptData(encryptedData, generateKey(password))
            db = TinyDB(storage=MemoryStorage)  # type: ignore
            db.storage.write(json.loads(decryptedData))  # Load decrypted data into TinyDB
            drawersTable = db.table('drawers')
            return db, drawersTable
```
- Tries to decrypt the encrypted data using the provided password. 
- If successful, initializes a TinyDB instance using in-memory storage.
- Loads the decrypted data into the TinyDB instance.
- Retrieves the `drawers` table from the TinyDB instance.
- Returns the TinyDB instance and the `drawers` table.

```python
        except Exception as e:
            sg.popup_error("Invalid password or data corrupted!", str(e))
            return None, None
```
- If an error occurs during decryption or data loading, it shows an error popup and returns `None` for both the TinyDB instance and the `drawers` table.

```python
    else:
        db = TinyDB(filePath)
        drawersTable = db.table('drawers')
        return db, drawersTable
```
- If the file does not exist, initializes a new TinyDB instance with the file path.
- Retrieves the `drawers` table from the new TinyDB instance.
- Returns the new TinyDB instance and the `drawers` table.

### Function: `saveData`

```python
def saveData(username, password, db):
    """
    Save data from a TinyDB instance to a file, encrypting it.

    Args:
        username (str): The username to determine the file name.
        password (str): The password to encrypt the data.
        db (TinyDB): The TinyDB instance containing the data.
    """
```
- This function saves the data from a TinyDB instance to a file, encrypting it using the provided password.

```python
    if not os.path.exists(dataFolder):
        os.makedirs(dataFolder)
```
- Checks if the directory for storing data files (`dataFolder`) exists. If it doesn't, it creates the directory.

```python
    filePath = os.path.join(dataFolder, f"{username}.json")
```
- Constructs the file path for the user's data file using the username. The file will be named `<username>.json` and located in the `dataFolder`.

```python
    data = json.dumps(db.storage.read())  # Serialize the data from TinyDB
    encryptedData = encryptData(data, generateKey(password))
    with open(filePath, 'w') as file:
        file.write(encryptedData)
```
- Serializes the data from the TinyDB instance to a JSON string.
- Encrypts the JSON string using the provided password.
- Opens the file in write mode and writes the encrypted data to the file.

### Function: `readData`

```python
def readData():
    """
    Read and return all data from the drawers table.

    Returns:
        dict: The data from the drawers table.
    """
```
- This function reads and returns all data from the `drawers` table in the TinyDB instance.

```python
    data = {}
    for item in drawersTable.all():
        data[item['drawer']] = item['items']
    return data
```
- Initializes an empty dictionary to store the data.
- Iterates over all items in the `drawers` table.
- For each item, adds an entry to the dictionary with the drawer name as the key and the list of items as the value.
- Returns the dictionary containing all the drawer data.

### Function: `writeData`

```python
def writeData(data):
    """
    Write data to the drawers table.

    Args:
        data (dict): The data to write to the drawers table.
    """
```
- This function writes the provided data to the `drawers` table in the TinyDB instance.

```python
    drawersTable.truncate()  # Clear the table first
    for key, items in data.items():
        drawersTable.insert({'drawer': key, 'items': items})
```
- Clears the `drawers` table to remove any existing data.
- Iterates over the provided data dictionary.
- For each entry, inserts a new item into the `drawers` table with the drawer name and list of items.

### Function: `popup`

```python
def popup(title, message):
    """
    Create a popup window with a message.

    Args:
        title (str): The title of the popup window.
        message (str): The message to display in the popup window.
    """
```
- This function creates and displays a popup window with the specified title and message.

```python
    layout = [
        [sg.Text(message)],
        [sg.Button('OK')]
    ]
```
- Defines the layout of the popup window with a text element displaying the message and an "OK" button.

```python
    window = sg.Window(title, layout, modal=True)
```
- Creates a window with the specified title and layout. The `modal=True` argument makes the window modal, meaning it will block interaction with other windows until it is closed.

```python
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED or event == 'OK':
            break
    window.close()
```
- Enters a loop to handle events from the popup window.
- If the window is closed or the "OK" button is pressed, it breaks out of the loop and closes the window.

