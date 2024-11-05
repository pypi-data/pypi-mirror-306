# RedPanPy Module Documentation

## Introduction

The `RedPanPy` module provides a framework for creating desktop GUI applications using Python and HTML. It leverages PyQt5's `QWebEngineView` to render HTML content and enables communication between Python and JavaScript using `QWebChannel`. This allows developers to build the UI with familiar web technologies (HTML, CSS, JavaScript) and handle logic in Python.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Module Overview](#module-overview)
   - [RedPanPyApp Class](#redpanpyapp-class)
   - [CallHandler Class](#callhandler-class)
4. [Usage Guide](#usage-guide)
   - [Initializing the Application](#initializing-the-application)
   - [Binding Events](#binding-events)
   - [Manipulating HTML Elements](#manipulating-html-elements)
   - [Getting Element Values](#getting-element-values)
   - [Running the Application](#running-the-application)
5. [Full Example](#full-example)
6. [Advanced Usage](#advanced-usage)
   - [Using Decorators for Binding](#using-decorators-for-binding)
   - [Handling Timers and Real-Time Updates](#handling-timers-and-real-time-updates)
7. [Security Considerations](#security-considerations)
8. [Conclusion](#conclusion)
9. [Appendix](#appendix)
   - [Adding `qwebchannel.js`](#adding-qwebchanneljs)

---

## Installation

Before using the `RedPanPy` module, ensure that you have the necessary dependencies installed:

```bash
pip install PyQt5 PyQtWebEngine
```

---

## Quick Start

Here's a minimal example to get you started:

```python
from RedPanPy import RedPanPyApp

def main():
    app = RedPanPyApp("index.html")

    def on_button_click():
        print("Button clicked!")
        app.set_element_text("message", "Button was clicked!")

    app.bind("myButton", "click", on_button_click)
    app.run()

if __name__ == "__main__":
    main()
```

---

## Module Overview

### `RedPanPyApp` Class

This is the main class that manages the PyQt application, loads the HTML file, and handles communication between Python and JavaScript.

**Constructor:**

```python
RedPanPyApp(html_path)
```

- `html_path`: Path to the HTML file to be loaded in the application.

**Methods:**

- `bind(element_id, event_type, callback)`: Binds an event of an HTML element to a Python callback function.
- `set_element_text(element_id, text)`: Sets the `innerHTML` of an HTML element.
- `get_element_text(element_id, callback)`: Retrieves the `innerHTML` of an HTML element.
- `get_element_value(element_id, callback)`: Retrieves the `value` of an HTML input element.
- `run()`: Starts the PyQt application and displays the window.

### `CallHandler` Class

An internal class that handles interactions from JavaScript. It registers callbacks and is called when events occur in the HTML.

**Methods:**

- `call(element_id, event_type)`: Invoked from JavaScript when an event occurs.
- `register_callback(element_id, event_type, callback)`: Registers a Python callback for a specific element and event type.

---

## Usage Guide

### Initializing the Application

To start using `RedPanPy`, you need to create an instance of `RedPanPyApp` with the path to your HTML file:

```python
app = RedPanPyApp("index.html")
```

This will:

- Initialize the PyQt application.
- Set up the main window.
- Load the specified HTML file into a `QWebEngineView`.
- Set up the communication channel between Python and JavaScript.

### Binding Events

To respond to events from HTML elements (e.g., button clicks), you can bind them to Python functions using the `bind` method:

```python
def on_button_click():
    print("Button was clicked!")

app.bind("myButton", "click", on_button_click)
```

- `element_id`: The `id` attribute of the HTML element.
- `event_type`: The type of event (e.g., `"click"`, `"input"`).
- `callback`: The Python function to be called when the event occurs.

**Example:**

In your HTML:

```html
<button id="myButton">Click Me</button>
```

In Python:

```python
def on_button_click():
    print("Button was clicked!")

app.bind("myButton", "click", on_button_click)
```

### Manipulating HTML Elements

You can modify the content of HTML elements from Python using the `set_element_text` method:

```python
app.set_element_text("message", "Hello, World!")
```

- `element_id`: The `id` attribute of the HTML element.
- `text`: The text or HTML content to set.

**Example:**

In your HTML:

```html
<div id="message"></div>
```

In Python:

```python
app.set_element_text("message", "Welcome to RedPanPy!")
```

### Getting Element Values

To retrieve values from HTML input elements, use the `get_element_value` method:

```python
def handle_value(value):
    print("Input value:", value)

app.get_element_value("myInput", handle_value)
```

- `element_id`: The `id` attribute of the HTML input element.
- `callback`: The Python function to receive the value.

**Example:**

In your HTML:

```html
<input type="text" id="myInput">
```

In Python:

```python
def handle_value(value):
    print("You entered:", value)

app.get_element_value("myInput", handle_value)
```

### Running the Application

To start the application and display the window, call the `run` method:

```python
app.run()
```

This will enter the PyQt event loop and keep the application running until it is closed.

---

## Full Example

Here's a complete example that ties everything together.

### index.html

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>RedPanPy Example</title>
</head>
<body>
    <h1 id="message">Hello!</h1>
    <button id="myButton">Click Me</button>
    <input type="text" id="myInput" placeholder="Type something...">
</body>
</html>
```

### main.py

```python
from RedPanPy import RedPanPyApp

def main():
    app = RedPanPyApp("index.html")

    def on_button_click():
        print("Button clicked!")
        app.set_element_text("message", "Button was clicked!")

    def on_input_change():
        def handle_value(value):
            print("Input changed to:", value)
            app.set_element_text("message", f"You typed: {value}")
        app.get_element_value("myInput", handle_value)

    app.bind("myButton", "click", on_button_click)
    app.bind("myInput", "input", on_input_change)

    app.run()

if __name__ == "__main__":
    main()
```

**Explanation:**

- Binds a click event on a button to `on_button_click`.
- Binds an input event on a text input to `on_input_change`.
- `on_input_change` retrieves the current value of the input field and updates the message.

---

## Advanced Usage

### Using Decorators for Binding

To simplify event binding, you can use decorators. Here's how you might modify your code:

```python
def bind(element_id, event_type):
    def decorator(func):
        app.bind(element_id, event_type, func)
        return func
    return decorator

@bind("myButton", "click")
def on_button_click():
    print("Button clicked!")
```

This approach keeps the binding close to the function definition and can make the code cleaner.

### Handling Timers and Real-Time Updates

If you need to update the UI at regular intervals (e.g., real-time clocks, live data updates), you can use PyQt's `QTimer`:

```python
from PyQt5.QtCore import QTimer

def update_time():
    from datetime import datetime
    current_time = datetime.now().strftime("%H:%M:%S")
    app.set_element_text("clock", current_time)

timer = QTimer()
timer.timeout.connect(update_time)
timer.start(1000)  # Update every second
```

In your HTML:

```html
<div id="clock"></div>
```

---

## Security Considerations

When using methods like `eval()` to execute code based on user input, there are security risks. Always sanitize and validate user inputs. Consider using safe evaluation methods or libraries designed for parsing mathematical expressions.

---

## Conclusion

The `RedPanPy` module allows you to create rich GUI applications using web technologies for the UI and Python for the logic. By understanding how to bind events, manipulate HTML elements, and interact between Python and JavaScript, you can build powerful desktop applications.

---

## Appendix

### Adding `qwebchannel.js`

To enable communication between Python and JavaScript, PyQt uses `qwebchannel.js`. Ensure that this file is available and loaded in your HTML.

**Steps:**

1. Locate `qwebchannel.js` in your PyQt installation directory, usually under `PythonXY/Lib/site-packages/PyQt5/Qt5/qml/QtWebChannel`.
2. Copy `qwebchannel.js` to your project directory or make sure your code can access it.
3. In `RedPanPyApp.register_binds()`, the code reads `qwebchannel.js` and injects it into the web page.

**Code Snippet:**

```python
def register_binds(self):
    with open('qwebchannel.js', 'r') as f:
        js_code = f.read()
    self.browser.page().runJavaScript(js_code)
    # Initialize the QWebChannel
    js_code = """
    if (typeof channelInitialized === 'undefined') {
        channelInitialized = true;
        new QWebChannel(qt.webChannelTransport, function(channel) {
            window.handler = channel.objects.handler;
        });
    }
    """
    self.browser.page().runJavaScript(js_code)
```

---

## Complete API Reference

### `RedPanPyApp` Class

#### Constructor

```python
RedPanPyApp(html_path)
```

- **Parameters:**
  - `html_path` (str): Path to the HTML file to be loaded.

#### Methods

##### `bind(element_id, event_type, callback)`

Binds an event of an HTML element to a Python callback.

- **Parameters:**
  - `element_id` (str): The `id` of the HTML element.
  - `event_type` (str): The type of event to listen for (e.g., `"click"`, `"input"`).
  - `callback` (function): The Python function to call when the event occurs.

**Usage:**

```python
def on_click():
    print("Element clicked!")

app.bind("elementId", "click", on_click)
```

##### `set_element_text(element_id, text)`

Sets the `innerHTML` of an HTML element.

- **Parameters:**
  - `element_id` (str): The `id` of the HTML element.
  - `text` (str): The text or HTML content to set.

**Usage:**

```python
app.set_element_text("message", "Hello, World!")
```

##### `get_element_text(element_id, callback)`

Retrieves the `innerHTML` of an HTML element.

- **Parameters:**
  - `element_id` (str): The `id` of the HTML element.
  - `callback` (function): The function to receive the text content.

**Usage:**

```python
def handle_text(text):
    print("Element text:", text)

app.get_element_text("message", handle_text)
```

##### `get_element_value(element_id, callback)`

Retrieves the `value` of an HTML input element.

- **Parameters:**
  - `element_id` (str): The `id` of the HTML input element.
  - `callback` (function): The function to receive the input value.

**Usage:**

```python
def handle_value(value):
    print("Input value:", value)

app.get_element_value("inputId", handle_value)
```

##### `run()`

Starts the PyQt application and displays the window.

**Usage:**

```python
app.run()
```

---

### `CallHandler` Class

An internal class used by `RedPanPyApp` to handle callbacks from JavaScript.

#### Methods

##### `call(element_id, event_type)`

Called from JavaScript when an event occurs.

- **Parameters:**
  - `element_id` (str): The `id` of the HTML element.
  - `event_type` (str): The type of event that occurred.

##### `register_callback(element_id, event_type, callback)`

Registers a callback function for a specific element and event.

- **Parameters:**
  - `element_id` (str): The `id` of the HTML element.
  - `event_type` (str): The type of event.
  - `callback` (function): The Python function to call.

---

**Note:** The `CallHandler` class is typically not used directly. Instead, use the `bind` method of `RedPanPyApp` to register event handlers.

---

## Final Remarks

By following this documentation, you should be able to:

- Set up a basic GUI application using `RedPanPy`.
- Bind HTML element events to Python functions.
- Manipulate the HTML content from Python.
- Retrieve values from HTML input elements.
- Utilize advanced features like decorators and timers.

Remember to always keep security in mind when dealing with user inputs and executing code.

Happy coding with `RedPanPy`!