import sounddevice as sd
import numpy as np
import speech_recognition as sr
import matplotlib.pyplot as plt
import cv2
from easygui import *
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string
import time

# Initialize recognizer instance
r = sr.Recognizer()

# Function to record audio with sounddevice and recognize speech
def func():
    isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
               'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
               'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
               'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
               'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
               'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
               'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
               'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
               'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
               'shall we go together tomorrow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
               'what are you doing']
    
    arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    while True:
        print("I am Listening...")
        
        # Record audio using sounddevice
        audio_data = sd.rec(int(5 * 44100), samplerate=44100, channels=2, dtype='int16')
        sd.wait()  # Wait until recording is finished
        
        # Convert audio to text using speech recognition
        try:
            # Using a temporary file to save the recording and recognize speech
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data)
            audio_file = sr.AudioFile("temp_audio.wav")
            with audio_file as source:
                audio = r.record(source)  # Record audio from the file
            text = r.recognize_google(audio)
            text = text.lower()
            print('You said:', text)
            
            for c in string.punctuation:
                text = text.replace(c, "")
                
            if text in isl_gif:
                # Code for showing GIF based on the speech
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
                lbl.load(r'ISL_Gifs/{0}.gif'.format(text))
                root.mainloop()
            else:
                # For alphabet handling (sign language)
                for i in range(len(text)):
                    if text[i] in arr:
                        image_address = 'letters/' + text[i] + '.jpg'
                        img = Image.open(image_address)
                        img_numpy = np.asarray(img)
                        plt.imshow(img_numpy)
                        plt.draw()
                        plt.pause(0.8)
                    else:
                        continue
        except Exception as e:
            print("Error:", e)
            time.sleep(1)  # Add delay in case of error

        plt.close()


# GUI with easygui for controlling the process
while True:
    image = "signlang.png"
    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Live Voice", "All Done!"]
    reply = buttonbox(msg, image=image, choices=choices)

    if reply == choices[0]:
        func()
    elif reply == choices[1]:
        break
