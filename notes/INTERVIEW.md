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

### Code Explanation

#### Handling "New Drawer" Event

```python
if event == "New Drawer":
```
- This line checks if the event triggered is the "New Drawer" button being clicked.

#### Getting Drawer Name

```python
    drawerName = sg.popup_get_text("Enter the drawer name:")
```
- Prompts the user to enter the name of the new drawer through a popup input dialog.
- The entered drawer name is stored in the variable `drawerName`.

```python
    if drawerName:
```
- Checks if a drawer name was entered (i.e., `drawerName` is not `None` or an empty string).

#### Check for Existing Drawer

```python
        if drawerName in data:
```
- Checks if a drawer with the entered name already exists in the data dictionary.

```python
            if sg.popup_yes_no(f"Drawer '{drawerName}' already exists. Do you want to overwrite it?") == 'No':
                continue
```
- If the drawer already exists, prompts the user with a Yes/No question asking if they want to overwrite the existing drawer.
- If the user selects "No," the code continues to the next iteration of the loop, effectively canceling the creation of a new drawer.

#### Getting First Object for Drawer

```python
        objectName = sg.popup_get_text("Enter the first object name for the drawer:")
```
- Prompts the user to enter the name of the first object to be added to the new drawer.

```python
        if objectName:
```
- Checks if an object name was entered (i.e., `objectName` is not `None` or an empty string).

```python
            quantity = sg.popup_get_text("Enter the quantity for the item:")
```
- Prompts the user to enter the quantity of the first object.

```python
            if quantity and quantity.isdigit():
```
- Checks if a quantity was entered and if it is a valid integer (using `isdigit()`).

#### Adding First Object to Drawer

```python
                data[drawerName] = [{'name': objectName, 'quantity': int(quantity)}]
```
- Creates a new entry in the `data` dictionary for the new drawer with the entered object name and quantity.
- The quantity is converted to an integer using `int(quantity)`.

#### Adding More Objects

```python
                while sg.popup_yes_no("Do you want to add another object?") == 'Yes':
```
- Prompts the user with a Yes/No question asking if they want to add another object to the drawer.
- If the user selects "Yes," the loop continues; otherwise, it exits the loop.

```python
                    objectName = sg.popup_get_text("Enter the next object name:")
```
- Prompts the user to enter the name of the next object to be added to the drawer.

```python
                    if objectName:
```
- Checks if an object name was entered.

```python
                        quantity = sg.popup_get_text("Enter the quantity for the item:")
```
- Prompts the user to enter the quantity of the next object.

```python
                        if quantity and quantity.isdigit():
```
- Checks if a quantity was entered and if it is a valid integer.

```python
                            data[drawerName].append({'name': objectName, 'quantity': int(quantity)})
```
- Adds the new object and its quantity to the list of objects for the drawer in the `data` dictionary.

```python
                        else:
                            popup("Error", "Quantity must be a number!")
                            break
```
- If the entered quantity is not a valid integer, shows an error popup and breaks out of the loop.

#### Writing Data and Success Popup

```python
                writeData(data)
                popup("Success", "Drawer and objects added successfully!")
```
- Calls `writeData(data)` to save the updated data to the database.
- Shows a success popup message indicating that the drawer and its objects were added successfully.

#### Error Handling for Invalid Quantity

```python
            else:
                popup("Error", "Quantity must be a number!")
```
- If the entered quantity is not a valid integer, shows an error popup indicating that the quantity must be a number.