import pygame
from state import State
import constants
from game_world import Game_World

class BeginDialogue(State):
    def __init__(self, game, player_name, gender):
        State.__init__(self, game)
        self.player_name = player_name
        self.gender = gender 
        self.attack_menu_bg = pygame.image.load("bgimg/attackmenubg.png").convert_alpha()
        self.attack_menu_img = pygame.transform.scale(self.attack_menu_bg, (800, 150))
        self.attack_menu_rect = self.attack_menu_img.get_rect()
        self.cursor_img = pygame.image.load("bgimg/cursor.png").convert_alpha()
        self.cursor_img  = pygame.transform.rotate(self.cursor_img, 90)
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_y = self.attack_menu_rect.y + 260
        self.cursor_rect.x, self.cursor_rect.y = self.attack_menu_rect.x + 750, self.cursor_pos_y
        self.message1 = False
        self.message2 = False
        self.current_time = pygame.time.get_ticks()
    
    def update(self, delta_time, actions):
        global game_world 
        if self.message1 == True and self.message2 == True and actions['start']:
            game_world = Game_World(self.game, self.player_name, self.gender)
            game_world.enter_state() 
        elif self.message1 == True and actions['start']:
            self.message2 = True
            self.current_time = pygame.time.get_ticks()
        elif actions['start']:
            self.message1 = True
            self.current_time = pygame.time.get_ticks()
        self.game.reset_keys()
        
    def draw(self, display):
        delay = 3000 
        if self.message2 == True and self.message1 == True:
            display.blit(self.attack_menu_img, (0, 150))
            self.game.draw_text(display, "and get out of here!", constants.WHITE, 400, 150 + 30)
            display.blit(self.cursor_img, self.cursor_rect)

        elif self.message1 == True:
            display.blit(self.attack_menu_img, (0, 150))
            self.game.draw_text(display, "I need to find out what's going on.", constants.WHITE, 400, 150 + 30)
            if pygame.time.get_ticks() - self.current_time > delay:
                self.game.draw_text(display, "I need to find out who I am.", constants.WHITE, 400, 150 + 65)
                if pygame.time.get_ticks() - self.current_time > delay * 2:
                    self.game.draw_text(display, "Time to make like a tree...", constants.WHITE, 400, 150 + 100)
                    display.blit(self.cursor_img, self.cursor_rect)
        else:
            display.fill((0,0,0))
            display.blit(self.attack_menu_img, (0, 150))
            self.game.draw_text(display, "Where am I?", constants.WHITE, 400, 150 + 30)
            if pygame.time.get_ticks() - self.current_time > delay:
                self.game.draw_text(display, "Why can't I remember anything?", constants.WHITE, 400, 150 + 65)
                if pygame.time.get_ticks() - self.current_time > delay * 2:
                    self.game.draw_text(display, "Who dropped the key to my shackles?", constants.WHITE, 400, 150 + 100)
                    display.blit(self.cursor_img, self.cursor_rect)
                
        
            

    