
# Closetman

Closetman is an inventory management tool designed for organizing electrical components or any other items in your closets. It features a user-friendly GUI built with PySimpleGUI and integrates data encryption, file management, and even a mini-game for light entertainment.

## Installation

Before running the `closetman.py` file, ensure you have Python installed on your system and the following libraries:

- PySimpleGUI
- TinyDB
- Cryptography
- Pygame

You can install these libraries using pip:

```bash
pip install PySimpleGUI tinydb cryptography pygame
```

## Running the Program

To start the program, navigate to the directory containing `closetman.py` and run:

```bash
python closetman.py
```

## How It Works

Upon launching, you will be prompted to enter a username and password. This information is used to create or access your personalized data file. Data is encrypted and saved locally, ensuring your inventory information is secure and private.

### Main Features

After logging in, you will be presented with several options:

- **New Drawer**: Create a new drawer with items. Specify item names and quantities.
- **Add/Remove Item**: Add or remove items in an existing drawer.
- **Search for Item**: Search for specific items across all drawers to see their quantities and locations.
- **Display Drawer**: Select and view the contents of a specific drawer.
- **Remove Drawer**: Completely remove an existing drawer and its contents.

Each of these functions is accessed via a button on the main GUI. Input validation is performed to ensure data integrity, such as verifying numeric input for item quantities.

### Additional Features

- **Tired? Button**: When clicked, launches a simple game (`catch.py`) using Pygame for a relaxing break.

### User Data Security

The application uses the cryptography library's Fernet module to encrypt and decrypt your inventory data, ensuring that your information remains secure and private.

## Notes

Ensure all files related to this program, including `catch.py` and the images or data files used, are kept in the same directory as `closetman.py` for proper functionality.
