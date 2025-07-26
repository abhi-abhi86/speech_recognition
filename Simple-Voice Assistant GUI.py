import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import ttk, filedialog
import threading
import subprocess
import os

recognizer = sr.Recognizer()
speaker = pyttsx3.init()
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("400x330")
root.resizable(False, False)
root.configure(bg="#f0f4f8")
title_label = tk.Label(root, text="Voice Assistant", font=("Segoe UI", 18, "bold"), bg="#f0f4f8", fg="#333")
title_label.pack(pady=10)
output_label = tk.Label(root, text="Press the mic to speak", font=("Segoe UI", 13), bg="#f0f4f8", fg="#00695c", wraplength=350, justify="center")
output_label.pack(pady=10)
canvas = tk.Canvas(root, width=100, height=100, highlightthickness=0, bg="#f0f4f8")
canvas.pack(pady=10)
mic_circle = canvas.create_oval(20, 20, 80, 80, fill="#4dd0e1", outline="")
pulse_state = [1]
progress = ttk.Progressbar(root, mode='indeterminate', length=300)
progress.pack(pady=10)
def pulse():
    r = 30 + 5 * pulse_state[0]
    canvas.coords(mic_circle, 50 - r/2, 50 - r/2, 50 + r/2, 50 + r/2)
    pulse_state[0] *= -1
    root.after(500, pulse)

pulse()
def handle_command(text):
    text = text.lower()

    if "notepad" in text:
        speaker.say("Opening Notepad")
        subprocess.Popen("notepad.exe")
    elif "calculator" in text:
        speaker.say("Opening Calculator")
        subprocess.Popen("calc.exe")
    elif "chrome" in text:
        speaker.say("Opening Chrome")
        subprocess.Popen("chrome.exe") 
    elif "open file" in text or "open a file" in text:
        speaker.say("Please choose a file to open")
        speaker.runAndWait()
        file_path = filedialog.askopenfilename()
        if file_path:
            os.startfile(file_path)
            speaker.say("Opening file")
        else:
            speaker.say("No file selected")
    else:
        speaker.say("Sorry, I don't recognize that command.")
    
    speaker.runAndWait()
def listen_and_speak():
    try:
        progress.start()
        output_label.config(text="Listening...")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            output_label.config(text="Recognizing...")
            text = recognizer.recognize_google(audio)
            output_label.config(text=f"You said:\n{text}")
            handle_command(text)

    except sr.UnknownValueError:
        output_label.config(text="Sorry, I didn't catch that.")
        speaker.say("Sorry, I could not understand what you said.")
        speaker.runAndWait()
    except sr.RequestError:
        output_label.config(text="Speech recognition service error.")
        speaker.say("There was an issue with the recognition service.")
        speaker.runAndWait()
    finally:
        progress.stop()

def start_listening():
    threading.Thread(target=listen_and_speak).start()
listen_button = tk.Button(
    root, text="Start Listening", font=("Segoe UI", 12),
    command=start_listening, bg="#00796b", fg="white",
    activebackground="#004d40", padx=15, pady=8, bd=0, relief="flat", cursor="hand2"
)
listen_button.pack(pady=10)

root.mainloop()
