import speech_recognition as sr
from time import ctime
import time
import os
import pygame
import sys
from pygame.math import Vector2 as vector
import csv
import json

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

otklik = {'Привет':{'otvet':'как дела?'},
		'нормально':{'otvet':'у меня тоже'}}


pygame.init()
pygame.mixer.init()
font = pygame.font.SysFont("Arial", 48)


class Recog:
    def __init__(self):
        super().__init__()
        self.speak = True
        self.speak_time = None
        self.speak_cooldown = 200

        self.save = True
        self.save_time = None
        self.save_cooldown = 2000

        self.sanat = []
               
    def recordAudio(self):
        pygame.key.set_repeat()
        r = sr.Recognizer()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.speak:
            with sr.Microphone() as source:
                try:
                    audio = r.listen(source)
                    data = r.recognize_google(audio, language="ru")
                    self.sanat.append(str(data))
                    return data

                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    pass
            self.speak_time = pygame.time.get_ticks()
        


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.speak:
            if current_time - self.speak_time >= self.speak_cooldown:
                self.speak = False

class Game(Recog):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Kielipeli')
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()

    def render(self,x):
        return font.render(x, 1, (255,255,255))
    
  
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open('sanasto.csv','a', encoding='utf8') as file:
                        sanasto = [str(self.sanat)]
                        writer = csv.writer(file)
                        writer.writerow(sanasto)
                    pygame.quit()
                    sys.exit()
            self.display_surface.fill('black')
            dt = self.clock.tick() / 1000
            data = self.recordAudio()
            text_surface = self.render(data)
            self.display_surface.blit(text_surface, (0,50))
            if data in otklik:
                resp_surface = self.render(otklik[data]['otvet'])
                self.display_surface.blit(resp_surface, (0,100))
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)


            pygame.display.update()

if __name__=='__main__':
    game = Game()
    game.run()


