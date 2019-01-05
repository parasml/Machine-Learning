#from gtts import gTTS


import os
import sys
import pyttsx3

def playGoogleAudio():

    #tts = gTTS(text='Good morning', lang='en')
    #tts.save("good.mp3")
    #os.system("mpg321 good.mp3")
    pass

def PlayMachineAudio():
    engine = pyttsx3.init()
    #engine.say('hello world ')
    #engine.runAndWait()


PlayMachineAudio()