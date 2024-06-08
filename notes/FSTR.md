# F String
Using f-strings (formatted string literals) in Python is a modern and convenient way to embed expressions inside string literals, using curly braces `{}`. Introduced in Python 3.6, f-strings provide several advantages over older string formatting methods, such as `%` formatting and the `str.format()` method. Here's why using f-strings is often preferred:

### Advantages of f-strings

1. **Readability**:
   - F-strings make it easy to see which variables are being inserted into the string and where they are being placed.
   ```python
   name = "John"
   age = 30
   print(f"Hello, {name}. You are {age} years old.")
   ```
   This is much clearer compared to other methods:
   ```python
   print("Hello, {}. You are {} years old.".format(name, age))
   ```

2. **Conciseness**:
   - F-strings are more concise, reducing the amount of boilerplate code.
   ```python
   print(f"Hello, {name}.")
   ```
   Compared to:
   ```python
   print("Hello, {}.".format(name))
   ```

3. **Performance**:
   - F-strings are generally faster than the older formatting methods. This is because f-strings are evaluated at runtime and use the same speed as concatenation using the `+` operator, but with less overhead.
   ```python
   f"Hello, {name}"
   ```
   This is quicker than:
   ```python
   "Hello, {}".format(name)
   ```

4. **Expression Embedding**:
   - F-strings allow for the embedding of arbitrary expressions within the string. This can include function calls, arithmetic operations, and even conditional expressions.
   ```python
   print(f"5 + 3 is {5 + 3}")
   print(f"Lowercase of 'HELLO' is {'HELLO'.lower()}")
   ```

5. **Debugging**:
   - F-strings provide an easy way to include variable names and their values for debugging purposes.
   ```python
   print(f"{name=}, {age=}")
   ```
   This will output:
   ```
   name='John', age=30
   ```

### Example Usage in the Program

Here are a few examples within the context of your program where f-strings can improve readability and conciseness:

#### Popup Messages

Instead of:
```python
sg.popup(f"Drawer '{drawerName}' already exists. Do you want to overwrite it?")
```

You might use:
```python
sg.popup(f"Drawer '{drawerName}' already exists. Do you want to overwrite it?")
```

#### Success and Error Messages

Instead of:
```python
popup("Success", f"Object '{objectName}' added to drawer '{drawerName}'!")
```

You might use:
```python
popup("Success", f"Object '{objectName}' added to drawer '{drawerName}'!")
```

### Conclusion

Using f-strings in Python offers significant benefits in terms of readability, conciseness, performance, and ease of use. They allow you to embed expressions directly within string literals, making your code more intuitive and easier to maintain. Given these advantages, f-strings are generally the recommended way to handle string formatting in modern Python code.