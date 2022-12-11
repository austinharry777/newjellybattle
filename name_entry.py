import pygame 
from state import State
import constants 
from pygame import mixer 
import time
from gender import Gender 

class Name_Entry(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.title_img = pygame.image.load("img/title.png").convert_alpha()
        self.attack_menu_bg = pygame.image.load("bgimg/attackmenubg.png").convert_alpha()
        self.attack_menu_img = pygame.transform.scale(self.attack_menu_bg, (800, 150))
        self.name_select_music = pygame.mixer.Sound("music/Name_and_Gender.wav")
        self.name_select_music.set_volume(0.3)
        self.attack_menu_rect = self.attack_menu_img.get_rect()
        self.player_name = ""
        self.name_typed = False

    def update(self, delta_time, actions):
        self.name_typed = False
        if actions['start']:
            self.name_typed = True
            gender_state = Gender(self.game, self.player_name)
            gender_state.enter_state()
        
        self.game.reset_keys()
                
    def draw(self, display):
        self.name_select_music.play(-1)
        display.blit(self.title_img, (0,100))
        display.blit(self.attack_menu_img, (0,150))
        self.game.draw_text(display, "Welcome to JellyBattle!", constants.WHITE, 400, 150 + 30)
        self.game.draw_text(display, "Please type your name.", constants.WHITE, 400, 150 + 65)
        self.game.draw_text(display, self.player_name, constants.WHITE, 400, 150 + 100)
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif len(self.player_name) > 9:
                        self.player_name[:-9]
                    #elif event.key == pygame.K_RETURN:
                        #self.name_typed = True
                    elif self.name_typed == False:
                        self.player_name += event.unicode
                
        