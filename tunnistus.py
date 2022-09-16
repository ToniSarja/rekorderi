from urllib import response
import speech_recognition as sr
from time import ctime
import time
import os
import pygame
import sys
from settings_west import *
from pygame.math import Vector2 as vector


pygame.init()
pygame.mixer.init()
font = pygame.font.SysFont("Arial", 48)

slovo = {
    'Привет':{'otvet':'Как дела?'},
    'Нормально':{'otvet':'Тоже'},
    'Как тебя зовут':{'otvet':'Меня зовут Маша'},
    'Очень приятно':{'otvet':'Мне тоже'}

}

class Recog:
    def __init__(self):
        super().__init__()
        self.recordAudio()
        self.check()

    def recordAudio(self):
        r = sr.Recognizer()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            with sr.Microphone() as source:
                try:
                    audio = r.listen(source)
                    data = r.recognize_google(audio, language="ru")
                    return data

                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    pass
        
    def check(self):
        voice = self.recordAudio()
        if voice in slovo:
            return slovo[voice]['otvet']


class Game(Recog):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Western shooter')
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.recordAudio()
        self.check()

    def render(self,x):
        return font.render(x, 1, (255,255,255))

    def run(self):
        while True:                                              
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.display_surface.fill('black')
            dt = self.clock.tick() / 1000
            data = self.check()
            text_surface = self.render(data)
            self.display_surface.blit(text_surface, (0,50))
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)


            pygame.display.update()

if __name__=='__main__':
    game = Game()
    game.run()
