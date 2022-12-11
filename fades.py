import pygame
from state import State 
#from castlebattle import CastleBattle

class Cutscene_Fadein:
    def __init__(self, game, speed, x,y):
        self.game = game
        self.load_sprites()
        self.fade_rect = self.curr_image.get_rect()
        self.position_x, self.position_y = x,y
        self.speed = speed #0 = slower fade in, 1 = faster fade in 
        self.fade_complete = False 
        self.current_frame, self.last_frame_update = 0,0

    def update(self, delta_time, actions):
        self.animate(delta_time)

    def draw(self, display):
        display.blit(self.curr_image,(self.position_x, self.position_y))
        
    def animate(self, delta_time):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        #progress animation
        if self.fade_complete == True:
            self.curr_image = self.curr_anim_list[len(self.curr_anim_list) - 1]
        else:
            if self.speed == 0:
                if self.last_frame_update > .14:
                    self.last_frame_update = 0
                    self.current_frame = (self.current_frame + 1 )
                    self.curr_image = self.curr_anim_list[self.current_frame]
            elif self.speed == 1:
                if self.last_frame_update > .07:
                    self.last_frame_update = 0
                    self.current_frame = (self.current_frame + 1 )
                    self.curr_image = self.curr_anim_list[self.current_frame]
            
            if self.current_frame >= len(self.curr_anim_list) - 1: 
                self.current_frame = len(self.curr_anim_list) - 1
                self.fade_complete = True
        return self.fade_complete 

    def load_sprites(self):
        #make fade in animation sprite lists
        self.fade_in_sprites = []
        for i in range(25):
            fade_in = pygame.image.load(f"bgimg/cutscene_fadein/{i}.png").convert_alpha()
            self.fade_in_sprites.append(fade_in)
        self.curr_image = self.fade_in_sprites[0]
        self.curr_anim_list = self.fade_in_sprites



class Cutscene_Fadeout:
    def __init__(self, game, x,y):
        self.game = game
        self.load_sprites()
        self.fade_rect = self.curr_image.get_rect()
        self.position_x, self.position_y = x,y 
        self.fade_complete = False 
        self.current_frame, self.last_frame_update = 0,0

    def update(self, delta_time, actions):
        self.animate(delta_time)

    def draw(self, display):
        display.blit(self.curr_image,(self.position_x, self.position_y))
        
    def animate(self, delta_time):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        #progress animation
        if self.last_frame_update > .07:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame + 1 )
            self.curr_image = self.curr_anim_list[self.current_frame]
        if self.current_frame >= len(self.curr_anim_list) - 1: 
            self.current_frame = len(self.curr_anim_list) - 1
            self.fade_complete = True
        return self.fade_complete 

    def load_sprites(self):
        #make out animation sprite lists
        self.fade_out_sprites = []
        for i in range(25):
            fade_out = pygame.image.load(f"bgimg/cutscene_fadeout/{i}.png").convert_alpha()
            self.fade_out_sprites.append(fade_out)
        self.curr_image = self.fade_out_sprites[0]
        self.curr_anim_list = self.fade_out_sprites



class ScreenFadeIn(State):
    def __init__(self, game, x,y):
        State.__init__(self, game)
        self.game = game 
        self.load_sprites()
        self.fade_rect = self.curr_image.get_rect()
        self.position_x, self.position_y = x,y 
        self.fade_complete = False 
        self.current_frame, self.last_frame_update = 0,0
        
    def update(self, delta_time, actions):
        if self.fade_complete == True:
           self.exit_state()
        self.animate(delta_time)
                
    def draw(self, display):
        self.prev_state.draw(display)   
        display.blit(self.curr_image,(self.position_x, self.position_y))
    
    def animate(self, delta_time):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        #progress animation
        if self.last_frame_update > .05:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame + 1 )
            self.curr_image = self.curr_anim_list[self.current_frame]
        if self.current_frame >= len(self.curr_anim_list) - 1: 
            self.current_frame = len(self.curr_anim_list) - 1
            self.fade_complete = True
           
    def load_sprites(self):
        #make fade in and out animation sprite lists
        self.fade_in_sprites = []
        for i in range(0,16):
            fade_in = pygame.image.load(f"bgimg/fadein/{i}.png").convert_alpha()
            self.fade_in_sprites.append(fade_in)
        self.curr_image = self.fade_in_sprites[0]
        self.curr_anim_list = self.fade_in_sprites



class ScreenFadeOut(State):
    def __init__(self, game, x,y, jelly_type, next_state):
        self.jelly_type = jelly_type
        self.game = game
        self.load_sprites()
        self.fade_rect = self.curr_image.get_rect()
        self.position_x, self.position_y = x,y 
        self.fade_complete = False 
        self.current_frame, self.last_frame_update = 0,0
        self.battle_start_sound = pygame.mixer.Sound("music/battle_start.wav")
        self.battle_start_sound.set_volume(1)
        self.next_state = next_state #CastleBattle(self.game, jelly_type)
        
    def update(self, delta_time, actions):
        if self.fade_complete == True:
            self.next_state.enter_state()
        self.animate(delta_time)
                
    def draw(self, display):
        display.blit(self.curr_image,(self.position_x, self.position_y))
        #pygame.mixer.Channel(3).play(self.battle_start_sound)
            
    def animate(self, delta_time):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        #progress animation
        if self.last_frame_update > .05:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame + 1 )
            self.curr_image = self.curr_anim_list[self.current_frame]
        if self.current_frame >= len(self.curr_anim_list) - 1: 
            self.current_frame = len(self.curr_anim_list) - 1
            self.fade_complete = True
        return self.fade_complete
           
    def load_sprites(self):
        #make fade in and out animation sprite lists
        self.fade_out_sprites = []
        for i in range(0,17):
            fade_out = pygame.image.load(f"bgimg/fadeout/{i}.png").convert_alpha()
            self.fade_out_sprites.append(fade_out)
        self.curr_image = self.fade_out_sprites[0]
        self.curr_anim_list = self.fade_out_sprites






            
        
