from state import State
import pygame 
import constants
from batplayer import BatPlayer, BatJelly, DamageText
from fades import ScreenFadeIn, Cutscene_Fadeout
from game_over import GameOver




class CastleBattle(State):
    def __init__(self, game, jelly_type):
        State.__init__(self, game)
        #variable to spawn jelly from type of orthogonal sprite, carried from Jelly class to screenfadeout to here
        self.jelly_type = jelly_type
        if self.jelly_type == 0:
            self.name = "Strawberry"
        elif self.jelly_type == 1:
            self.name = "Grape"
        elif self.jelly_type == 2:
            self.name = "Peanut"
        #load images and assets here
        #background images
        self.dungeon_bg = pygame.image.load("bgimg/dungeonbg.png").convert_alpha()
        self.castle2bg = pygame.image.load("bgimg/castle2bg.png").convert_alpha()
        self.castle1bg = pygame.image.load("bgimg/castle1bg.png").convert_alpha()
        menu_bg = pygame.image.load("bgimg/battlemenubg.png").convert_alpha()
        attack_menu_bg = pygame.image.load("bgimg/attackmenubg.png").convert_alpha()
        #Initial battle menu and cursor position
        self.battle_menu_img = pygame.transform.scale(menu_bg, (800, 150))
        self.battle_menu_rect = self.battle_menu_img.get_rect()
        self.battle_menu_rect.topleft = ((0, 450))
        self.cursor_img = pygame.image.load("bgimg/cursor.png").convert_alpha()
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_y = self.battle_menu_rect.y + 15
        self.cursor_rect.x, self.cursor_rect.y = self.battle_menu_rect.x + 30, self.cursor_pos_y
        #attack menu
        self.attack_menu_img = pygame.transform.scale(attack_menu_bg, (800, 150))
        self.attack_menu_rect = self.attack_menu_img.get_rect()
        self.attack_menu_rect.topleft = ((0, 450))
        self.attack_cursor_img = pygame.transform.rotate(self.cursor_img, (270))
        self.attack_cursor_rect = self.attack_cursor_img.get_rect()
        self.attack_cursor_pos_y = 150
        self.cursor2_img = pygame.image.load("bgimg/cursor.png").convert_alpha()
        self.cursor2_rect = self.cursor2_img.get_rect()
        self.cursor2_pos_y = self.attack_menu_rect.y + 20
        self.cursor2_rect.x, self.cursor2_rect.y = self.attack_menu_rect.x + 30, self.cursor2_pos_y
        #item menu
        self.item_cursor_img = pygame.transform.rotate(self.cursor_img, (270))
        self.item_cursor_rect = self.attack_cursor_img.get_rect()
        self.item_cursor_pos_y = 150
        #menu options
        self.menu_options = {0: "Attack", 1: "Item", 2: "Run"}
        self.index = 0 
        #create player instance
        self.batplayer = BatPlayer(self.game, 200, 390,'Austin', 20, 100)
        #jelly instance
        self.batjelly = BatJelly(self.game, 685, 250, self.jelly_type, 50)
        #screen fade in bool and black timer
        self.fade_in = False 
        self.update_time = pygame.time.get_ticks()
        #variables for attack submenu
        self.attack_menu = False
        self.attack = False 
        #variables for item submenu
        self.item_menu = False
        self.item = False
        #victory variables
        self.victory = False
        self.victory_enter = False
        #battle variables
        self.current_fighter = 1
        self.total_fighters = 2
        self.action_cooldown = 0
        self.action_wait_time = 750
        self.battle_over = 0
        self.damage_text_group = pygame.sprite.Group()
        self.game_over_fadeout = Cutscene_Fadeout(self.game, 0,0)
    
    def update(self, delta_time, actions):
        self.batplayer.damage_text_group.update(delta_time)
        self.batjelly.damage_text_group.update(delta_time)
        self.batplayer.update(delta_time, actions)
        self.batjelly.update(delta_time,actions) 
        if self.fade_in == False:
            new_state = ScreenFadeIn(self.game, 0,0)
            new_state.enter_state()
            self.fade_in = True 
        if self.battle_over == 1:
            self.victory = True
            self.batplayer.action = 5
        elif self.battle_over == -1:
            pygame.mixer.fadeout(2000)
            self.action_cooldown += 1
            if self.action_cooldown >= self.action_wait_time:
                self.game_over_fadeout.update(delta_time, actions)
        elif self.battle_over == 0:
            if self.batplayer.alive == True:
                if self.current_fighter == 1:
                    self.action_cooldown += 1
                    
                    if self.action_cooldown >= self.action_wait_time:
                        if self.attack == True:
                            self.batplayer.attack(self.batjelly)
                            self.current_fighter += 1
                            self.action_cooldown = 0
                            self.attack_menu = False 
                            self.attack = False 
                        elif self.item == True and self.batplayer.potions > 0:
                            self.batplayer.use_potion()
                            self.current_fighter += 1
                            self.action_cooldown = 0
                            self.item_menu = False 
                            self.item = False
            
            else:
                self.battle_over = -1

            if self.current_fighter == 2:
                if self.batjelly.alive == True:
                    self.action_cooldown += 1
                    if self.action_cooldown >= self.action_wait_time:
                        self.batjelly.attack(self.batplayer)
                        self.current_fighter += 1
                        self.action_cooldown = 0
                else:
                    self.current_fighter += 1

            if self.current_fighter > self.total_fighters:
                self.current_fighter = 1

        alive_enemies = 0
        if self.batjelly.alive == True:
            alive_enemies += 1
        if alive_enemies == 0:
            self.battle_over = 1

        #check if battle is over
        # if self.battle_over != 0:
        #         if self.battle_over == -1:
        #             pass
        #         elif self.battle_over == 1:
        #             self.victory = True
                           
        
        
        
        if self.attack_menu == True and actions['action1'] == True:
            self.attack = True
        elif self.attack_menu == True and actions['action2'] == True:
            self.attack_menu = False
        
        if self.item_menu == True and actions['action1'] == True:
            self.item = True
        elif self.item_menu == True and actions['action2'] == True:
            self.item_menu = False
        if self.victory == True and actions['action1'] == True:
            self.victory_enter = True
            while len(self.game.state_stack) > 5:
                self.game.state_stack.pop()
                #game_world.enemy_list.pop()
        
        else:
            if actions['down'] == True:
                self.index = (self.index + 1) % len(self.menu_options)
            elif actions['up'] == True:
                self.index = (self.index - 1) % len(self.menu_options)
            elif actions['action1'] == True:
                if self.index == 0:
                    self.attack_menu = True
                
                elif self.index == 1:
                    self.item_menu = True
                    
                elif self.index == 2:
                    pass
            
                
            self.cursor_rect.y = self.cursor_pos_y + (self.index * 30)
        
        self.game.reset_keys()

    def draw(self, display):
        self.batplayer.damage_text_group.draw(display)
        self.batjelly.damage_text_group.draw(display)
        display.fill((0,0,0))
        if pygame.time.get_ticks() - self.update_time > 900:
            if self.batjelly.type == 0:
                display.blit(self.dungeon_bg, (0,0))
            elif self.batjelly.type == 1:
                display.blit(self.castle2bg, (0,0))
            elif self.batjelly.type == 2:
                display.blit(self.castle1bg, (0,0))
            display.blit(self.battle_menu_img, self.battle_menu_rect)
            display.blit(self.cursor_img, self.cursor_rect)
            self.batplayer.draw(display)
            self.batjelly.draw(display)
            #show player stats
            self.game.draw_text(display, f"{self.batplayer.player_name}", constants.WHITE, 440, 450 +25)
            self.game.draw_text(display, f"HP:{self.batplayer.hp}/{self.batplayer.max_hp}", constants.WHITE, 670, 450 +25)
            self.game.draw_text(display, f"MP:{self.batplayer.mp}/{self.batplayer.max_mp}", constants.WHITE, 670, 450 +55)
            #self.game.draw_text(display, f"SP", constants.WHITE, 345,490)
            self.game.draw_text(display, f"{self.name} Jelly", constants.WHITE, 550, (450 +115))
            #Choice menu
            self.game.draw_text(display, f"Attack", constants.WHITE, 120, 450 + 25)
            self.game.draw_text(display, f"Item", constants.WHITE, 95, 450 + 55)
            self.game.draw_text(display, f"Run", constants.WHITE, 90, 450 + 85)
            self.game.draw_text(display, f"  Magic", constants.GREY, 90, 450 + 115)
           
            if self.attack_menu == True:
                self.draw_attack_menu(display) 
            if self.item_menu == True:
                self.draw_item_menu(display)
            if self.victory == True:
                self.draw_victory_screen(display)
            if self.battle_over == -1:
                self.game_over_fadeout.draw(display)
                if self.game_over_fadeout.fade_complete == True:
                    game_over = GameOver(self.game)
                    game_over.enter_state()
               
                
                
            

    def draw_attack_menu(self, display):
        display.blit(self.attack_menu_img, self.attack_menu_rect)
        display.blit(self.attack_cursor_img, self.attack_cursor_rect)
        display.blit(self.cursor2_img, self.cursor2_rect)
        self.game.draw_text(display, f"{self.name} Jelly", constants.WHITE, 400, (450 +30))
        self.attack_cursor_rect.x, self.attack_cursor_rect.y = 675, self.attack_cursor_pos_y
        self.cursor2_rect.x, self.cursor2_rect.y = self.attack_menu_rect.x + 150, self.cursor2_pos_y

    def draw_item_menu(self, display):
        display.blit(self.attack_menu_img, self.attack_menu_rect)
        display.blit(self.item_cursor_img, self.item_cursor_rect)
        display.blit(self.cursor2_img, self.cursor2_rect)
        self.game.draw_text(display, f"Potions = {self.batplayer.potions}", constants.WHITE, 400, (450 +30))
        self.item_cursor_rect.x, self.item_cursor_rect.y = 180, self.item_cursor_pos_y
        self.cursor2_rect.x, self.cursor2_rect.y = self.attack_menu_rect.x + 150, self.cursor2_pos_y

    def draw_victory_screen(self, display):
        display.blit(self.attack_menu_img, (0,20))
        self.game.draw_text(display, f"Victory!", constants.WHITE, 400, (50))
        self.game.draw_text(display, f"{self.batplayer.player_name} gained 10 xp!", constants.WHITE, 400, (80))
        self.game.draw_text(display, f"{self.batplayer.player_name} is Level {self.batplayer.level}.", constants.WHITE, 400, (110))
        


        




        
        
    
       