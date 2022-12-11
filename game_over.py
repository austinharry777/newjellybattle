import pygame
from pygame import mixer 
from state import State
import constants
from fades import Cutscene_Fadein, Cutscene_Fadeout
mixer.init()

class GameOver(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game_over_img = pygame.image.load("bgimg/game_over.png").convert_alpha()
        self.game_over_music = pygame.mixer.Sound("music/Game_Over.wav")
        self.game_over_music.set_volume(0.3)
        self.font = pygame.font.Font('img/MMRock9.ttf', 22)
        self.cursor_img = pygame.image.load("bgimg/cursor.png").convert_alpha()
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_rect.x, self.cursor_rect.y = 110, 440 
        self.menu_options = {0: 'Continue From Last Save', 1: 'End'}
        self.cutscene_fadein = Cutscene_Fadein(self.game, 0, 0,0)
        self.cutscene_fadeout = Cutscene_Fadeout(self.game, 0,0)
        self.index = 0
        self.music_start = pygame.time.get_ticks()
        self.restart_game = False
    def update(self, delta_time, actions):
        if self.restart_game == True:
            self.cutscene_fadeout.update(delta_time, actions)
            self.game_over_music.fadeout(2000)
        self.cutscene_fadein.update(delta_time, actions)
        
        if actions['down'] == True:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions['up'] == True:
            self.index = (self.index - 1) % len(self.menu_options)

        if self.index == 0 and actions['start'] == True:
            pass
        elif self.index == 1 and actions['start'] == True:
            self.restart_game = True
            
        if self.cutscene_fadeout.fade_complete == True:
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()


        self.cursor_rect.y = 440 + (self.index * 50)

        self.game.reset_keys()
        
    
    def draw(self, display):
        
        song_length = 39000
        display.blit(self.game_over_img, (0,0))
        display.blit(self.cursor_img, self.cursor_rect)
        self.game_over_music.play() 
        if pygame.time.get_ticks() - self.music_start > song_length:
            self.game_over_music.stop()
        self.game.draw_text(display,'Continue From Last Save', constants.WHITE, 400, 450)
        self.game.draw_text(display,'End', constants.WHITE, 182, 500)
        self.cutscene_fadein.draw(display)
        if self.restart_game == True:
            self.cutscene_fadeout.draw(display)