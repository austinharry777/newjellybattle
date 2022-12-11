import pygame 
from state import State
import constants 
from pygame import mixer 
import time
from name_entry import Name_Entry
import dialogue 
import threading
mixer.init()


class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.title_img = pygame.image.load("img/title.png").convert_alpha()
        self.title_music = pygame.mixer.Sound("music/Welcome_to_JellyBattle.wav")
        self.title_music.set_volume(0.3)
        self.music_start = pygame.time.get_ticks()
        self.font = pygame.font.Font('img/MMRock9.ttf', 22)
        
    def update(self, delta_time, actions):
        
        if actions['start']:
            self.title_music.fadeout(2000)
            name_state = Name_Entry(self.game)
            name_state.enter_state()
        self.game.reset_keys()
            
    def draw(self, display):
        self.title_music.play()
        #set timer to stop repeating of title music, should only play once
        song_length = 9000
        if pygame.time.get_ticks() - self.music_start > song_length:
            self.title_music.stop()
        display.blit(self.title_img, (0,100))
        #self.game.draw_text(display,'Press Enter to Begin', constants.WHITE, 400, 350)
        self.text = self.game.draw_text_by_letter(display,  'Press Enter to Begin', constants.WHITE, 400, 350)
        self.text.update()     