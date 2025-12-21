import sounddevice as sd
import numpy as np
import speech_recognition as sr
import scipy.io.wavfile as wav
import time
import string
import tkinter as tk
from itertools import count
from PIL import Image, ImageTk

# Initialize recognizer instance
r = sr.Recognizer()

# List of common phrases in Indian Sign Language (for example)
isl_gif = ['hello', 'thank you', 'good morning', 'good night', 'how are you']

# Letters in the alphabet (for individual letter mapping)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Function to record audio with sounddevice and recognize speech
def func():
    while True:
        print("I am Listening...")

        # Record audio using sounddevice
        fs = 44100  # Sampling frequency
        audio_data = sd.rec(int(5 * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Save the recorded audio as a WAV file using scipy.io.wavfile
        wav.write('temp_audio.wav', fs, audio_data)

        # Convert audio to text using speech recognition
        try:
            audio_file = sr.AudioFile('temp_audio.wav')
            with audio_file as source:
                audio = r.record(source)  # Record audio from the file
            text = r.recognize_google(audio)
            text = text.lower()
            print('You said:', text)

            # Remove punctuation from the recognized text
            for c in string.punctuation:
                text = text.replace(c, "")

            # Check if the recognized text is a sign language phrase
            if text in isl_gif:
                show_sign_language_gif(text)
            else:
                # Check for individual letters
                for char in text:
                    if char in alphabet:
                        show_sign_language_image(char)
                    else:
                        continue
        except Exception as e:
            print("Error:", e)
            time.sleep(1)  # Add delay in case of error

# Function to show the GIF for recognized sign language phrases
def show_sign_language_gif(phrase):
    class ImageLabel(tk.Label):
        def load(self, im):
            if isinstance(im, str):
                im = Image.open(im)
            self.loc = 0
            self.frames = []

            try:
                for i in count(1):
                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                    im.seek(i)
            except EOFError:
                pass

            try:
                self.delay = im.info['duration']
            except:
                self.delay = 100

            if len(self.frames) == 1:
                self.config(image=self.frames[0])
            else:
                self.next_frame()

        def unload(self):
            self.config(image=None)
            self.frames = None

        def next_frame(self):
            if self.frames:
                self.loc += 1
                self.loc %= len(self.frames)
                self.config(image=self.frames[self.loc])
                self.after(self.delay, self.next_frame)

    root = tk.Tk()
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(f'ISL_Gifs/{phrase}.gif')  # Load the corresponding GIF
    root.mainloop()

# Function to show the image for recognized sign language letter
def show_sign_language_image(letter):
    image_address = f'letters/{letter}.jpg'
    img = Image.open(image_address)
    img.show()  # Display the image for the letter

# GUI with easygui for controlling the process
while True:
    reply = input("Press '1' for Live Voice or '2' to Exit: ")
    
    if reply == '1':
        func()
    elif reply == '2':
        break
