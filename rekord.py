import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os
import pygame


pygame.init()
Builder.load_file('rekord.kv')
mene = pygame.mixer.Sound('Go.mp3')
freq = 44100
duration = 5

class Plei(Screen):

    def soita(self):
        mene.play()

    
    def nauhoita(self):
        if os.path.exists("recording0.wav"):
            os.remove("recording0.wav")
        recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=2)
        sd.wait()
        try:
            write("recording0.wav", freq, recording)
        except:
            pass

    def kuuntele(self):
        nauha = pygame.mixer.Sound("recording0.wav")   
        try:
            nauha.play()
        except: 
            pass

    def vertaa(self):
        nauha = pygame.mixer.Sound("recording0.wav")
        try:
            mene.play()
        except:
            pass
        try:
            nauha.play()
        except:
            pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()