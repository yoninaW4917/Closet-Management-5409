### Code Explanation

#### User Authentication

```python
# Get username and password
username = sg.popup_get_text("Enter your username:")
if username is None:  # If the user cancels, exit the program
    exit()
```
- This block creates a popup to prompt the user for their username.
- If the user cancels or closes the popup, the program exits.

```python
password = sg.popup_get_text("Enter your password:", password_char='*')
if password is None:  # If the user cancels, exit the program
    exit()
```
- This block creates a popup to prompt the user for their password, masking the input with `*`.
- If the user cancels or closes the popup, the program exits.

#### Database Initialization

```python
# Initialize the database
db, drawersTable = loadData(username, password)
if db is None:
    exit()
```
- This initializes the database by calling `loadData` with the username and password.
- If the database cannot be loaded (e.g., due to incorrect password), the program exits.

#### Main GUI Layout

```python
# Main GUI layout
layout = [
    [sg.Text("Choose an option:")],
    [sg.Button("New Drawer"), sg.Button("Add/Remove Item"), sg.Button("Search for Item"), sg.Button("Display Drawer")],
    [sg.Button("Remove Drawer")], 
    [sg.Button("Tired?")],  # New Button
    [sg.Exit()]
]
```
- This defines the layout of the main GUI window with options for different actions.

```python
# Create the window
window = sg.Window("Drawer Management System", layout)
```
- This creates the main application window with the specified layout.

#### Event Loop

```python
# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        saveData(username, password, db)
        break
```
- This loop handles events (e.g., button clicks) in the GUI.
- If the window is closed or the "Exit" button is clicked, the data is saved and the loop breaks, ending the program.

```python
    data = readData()
```
- This reads all the data from the drawers table.

#### New Drawer

```python
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
```
- This block handles creating a new drawer.
- Prompts the user for a drawer name, checks if it exists, and prompts for item details.
- If the drawer already exists, asks if the user wants to overwrite it.
- Adds items to the drawer and writes the data back to the database.

#### Add/Remove Item

```python
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
```
- This block handles adding or removing items from a drawer.
- Prompts the user for the drawer name, checks if it exists, and prompts for action (add or remove).
- Handles adding items to the drawer and removing items from the drawer, updating the database accordingly.

#### Search for Item

```python
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
```
- This block handles searching for an item across all drawers.
- Prompts the user for the item name and searches through all drawers.
- Displays a popup with the search results.

#### Display Drawer

```python
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
```
- This block handles displaying the contents of a selected drawer.
- Prompts the user to select a drawer and displays its contents in a popup.

#### Remove Drawer

```python
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
```
- This block handles removing a selected drawer.
- Prompts the user to select a drawer and confirms the deletion.
- Removes the drawer and updates the database.

#### Tired?

```python
    elif event == "Tired?":
        subprocess.Popen(["python", "catch.py"])  # This line runs catch.py
```
- This block runs the `catch.py` script using `subprocess.Popen`.

#### Close Window

```python
window.close()
```
- This closes the main application window.