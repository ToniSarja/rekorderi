import speech_recognition as sr
from time import ctime
import time
import os
import pygame
import sys
from pygame.math import Vector2 as vector
import csv
import json
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import pylab
import matplotlib.backends.backend_agg as agg
import pygame
import pygame_menu

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
        self.speak_cooldown = 2000

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
            
    def cooldowns(self):
        self.speak_time = pygame.time.get_ticks()
        current_time = pygame.time.get_ticks()
        if self.speak:
            if current_time - self.speak_time >= self.speak_cooldown:
                self.speak = False
class Menu:
	def valikko(self):
		surface = pygame.display.set_mode((1000, 800))
		menu = pygame_menu.Menu('', 800, 600,
							theme=pygame_menu.themes.THEME_BLUE)

		table = menu.add.table(table_id='my_table', font_size=20)
		table.default_cell_padding = 5
		table.default_row_background_color = 'white'
		table.add_row(['First item', 'Second item', 'Third item'],
					cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)
		table.add_row(['A', 'B', 1])
		table.add_row(['α', 'β', 'γ'], cell_align=pygame_menu.locals.ALIGN_CENTER)
		menu.mainloop(surface)


class Game(Recog,Menu):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('Kielipeli')
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.game_paused = False

    def render(self,x):
        return font.render(x, 1, (255,255,255))

    def peruspeli(self):
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        with open('sanasto.csv','a', encoding='utf8') as file:
                            sanasto = [str(self.sanat)]
                            writer = csv.writer(file)
                            writer.writerow(sanasto)
                            self.valikko()
                else:
                    self.peruspeli()



            pygame.display.update()

if __name__=='__main__':
    game = Game()
    game.run()


