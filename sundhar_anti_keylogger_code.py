import tkinter as tk
from tkinter import *
from pynput import keyboard
import json

# Global variables
blocked_keys = set()
logging_enabled = True
output_file_txt = 'sundhar_anti-keylogger_output.txt'
output_file_json = 'sundhar_anti-keylogger_output.json'
logged_data = []
listener = None  # Variable to hold the keyboard listener instance

# Function to block specific keys
def block_keys(keys):
    blocked_keys.update(keys)

# Function to unblock specific keys
def unblock_keys(keys):
    blocked_keys.difference_update(keys)

# Function to check if a key is blocked
def is_key_blocked(key):
    return key in blocked_keys

# Function to handle key press event
def on_press(key):
    global logging_enabled, logged_data
    if logging_enabled and not is_key_blocked(key):
        logged_data.append({"event": "pressed", "key": str(key)})
        print(f"Key {key} pressed")

# Function to handle key release event
def on_release(key):
    global logging_enabled, logged_data
    if logging_enabled and not is_key_blocked(key):
        logged_data.append({"event": "released", "key": str(key)})
        print(f"Key {key} released")

# Function to toggle logging
def toggle_logging():
    global logging_enabled
    logging_enabled = not logging_enabled
    status_label.config(text="Logging enabled" if logging_enabled else "Logging disabled", fg="green" if logging_enabled else "red")
    if not logging_enabled:
        save_logs()

# Function to save logged data in TXT and JSON formats
def save_logs():
    with open(output_file_txt, 'w') as txt_file:
        for entry in logged_data:
            txt_file.write(f"{entry['event']}: {entry['key']}\n")
    
    with open(output_file_json, 'w') as json_file:
        json.dump(logged_data, json_file, indent=4)

# Function to start the keylogger
def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    status_label.config(text="Keylogger started", fg="green")

# Function to stop the keylogger
def stop_keylogger():
    global listener
    if listener and listener.is_alive():
        listener.stop()
        status_label.config(text="Keylogger stopped", fg="red")

# Function to display result
def display_result():
    result_window = Toplevel(root)
    result_window.title("Keylogger Result")
    result_window.geometry("300x200")
    result_text = Text(result_window)
    result_text.pack()
    for entry in logged_data:
        result_text.insert(END, f"{entry['event']}: {entry['key']}\n")

# GUI setup
root = Tk()
root.title("Anti-Keylogger System")
root.geometry("400x250")  # Larger window size

# Labels
status_label = Label(root, text="Logging enabled", fg="green")
status_label.pack()

# Buttons
block_button = Button(root, text="Block Keys", command=lambda: block_keys({'a', 'b', 'c'}))
block_button.pack(pady=5)

unblock_button = Button(root, text="Unblock Keys", command=lambda: unblock_keys({'a', 'b', 'c'}))
unblock_button.pack(pady=5)

toggle_button = Button(root, text="Toggle Logging", command=toggle_logging)
toggle_button.pack(pady=5)

start_button = Button(root, text="Start Keylogger", command=start_keylogger)
start_button.pack(pady=5)

stop_button = Button(root, text="Stop Keylogger", command=stop_keylogger)
stop_button.pack(pady=5)

result_button = Button(root, text="Display Result", command=display_result)
result_button.pack(pady=5)

root.mainloop()
