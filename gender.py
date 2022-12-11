import pygame
from state import State
import constants
from game_world import Game_World
from fades import Cutscene_Fadeout
from begindialogue import BeginDialogue

class Gender(State):
    def __init__(self, game, player_name):
        State.__init__(self, game)
        self.title_img = pygame.image.load("img/title.png").convert_alpha()
        self.attack_menu_bg = pygame.image.load("bgimg/attackmenubg.png").convert_alpha()
        self.attack_menu_img = pygame.transform.scale(self.attack_menu_bg, (800, 150))
        self.attack_menu_rect = self.attack_menu_img.get_rect()
        self.cursor_img = pygame.image.load("bgimg/cursor.png").convert_alpha()
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_y = self.attack_menu_rect.y + 205
        self.cursor_rect.x, self.cursor_rect.y = self.attack_menu_rect.x + 200, self.cursor_pos_y
        self.gender_options = {0: 'Female', 1: 'Male'}
        self.gender = 0 #0 is female, 1 is male.
        self.index = 0 
        self.gender_choice = False
        self.gender_message = False 
        self.player_name = player_name 
        self.cutscene_fadeout = Cutscene_Fadeout(self.game, 0,0)
        self.act1_screen = False
        
    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if self.index == 0 and actions['start']:
            self.gender = 0
            self.gender_choice = True
            
        elif self.index == 1 and actions['start']:
            self.gender = 1
            self.gender_choice = True
            
        elif actions['action2']:
            self.exit_state()
        
        if self.gender_choice == True and actions['action1']:
            self.gender_message = True

        if self.gender_message == True:
            pygame.mixer.fadeout(2000)
            self.cutscene_fadeout.update(delta_time, actions)
        if self.act1_screen == True:
            pygame.time.wait(4000)
            begin_state = BeginDialogue(self.game, self.player_name, self.gender) #Game_World(self.game, self.player_name, self.gender)
            begin_state.enter_state()    
               
        self.game.reset_keys()

    def draw(self, display):
        self.game.state_stack[-2].draw(display)
        self.prev_state.draw(display)
        display.blit(self.title_img, (0,100))
        display.blit(self.attack_menu_img, (0,150))
        self.game.draw_text(display, (f"Please choose a gender."), constants.WHITE, 400, 150 + 30)
        self.game.draw_text(display, "Female      Male", constants.WHITE, 400, 150 + 65)
        display.blit(self.cursor_img, self.cursor_rect)
        if self.gender_choice == True:
            display.blit(self.title_img, (0,100))
            display.blit(self.attack_menu_img, (0,150))
            self.game.draw_text(display, (f"Hello, {self.player_name}!"), constants.WHITE, 400, 150 + 30)
            self.game.draw_text(display, "It is time to begin.", constants.WHITE, 400, 150 + 65)
            self.game.draw_text(display, "Press 'p' when ready.", constants.WHITE, 400, 150 + 100)
        if self.gender_message == True:
            self.cutscene_fadeout.draw(display)
        if self.cutscene_fadeout.fade_complete == True:
            display.fill(constants.BLACK) 
            self.game.draw_text(display, "Act I:", constants.WHITE, 400, 150 + 65)
            self.game.draw_text(display, "Escape from Jelly Castle", constants.WHITE, 400, 150 + 100)
            self.act1_screen = True 
            
    def update_cursor(self, actions):
        if actions['right']:
            self.index = (self.index + 1) % len(self.gender_options)
        elif actions['left']:
            self.index = (self.index - 1) % len(self.gender_options)
        self.cursor_rect.x = (self.attack_menu_rect.x + 200) + (self.index * 265) 

    


