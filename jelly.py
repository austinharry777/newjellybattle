import pygame
import constants 
import math
from castlebattle import CastleBattle 
import time 
from pygame import mixer
from fades import ScreenFadeOut  
mixer.init()

class Jelly:
    def __init__(self, game, x,y, jelly_type):
        self.game = game
        self.jelly_type = jelly_type # 0:'strawberry',1:'grape',2:'peanut',3:'ancient'
        self.load_sprites()
        self.jelly_rect = self.curr_image.get_rect(center=(x,y))
        self.position_x, self.position_y = x,y 
        self.current_frame, self.last_frame_update = 0,0
        self.flip = False
        self.battle_bool = False
        self.battle_start_sound = pygame.mixer.Sound("music/battle_start.wav")
        self.battle_start_sound.set_volume(1) 
        
    def update(self,delta_time, player, screen_scroll):
        self.position_x += screen_scroll[0]
        self.position_y += screen_scroll[1]
        dx = 0
        dy = 0
        #Check distance to player
        dist = math.sqrt(((self.position_x - player.position_x) ** 2) + ((self.position_y - player.position_y) ** 2))
        if dist < constants.RANGE:
            if self.position_x > player.position_x:
                dx = -constants.ENEMY_SPEED
            if self.position_x < player.position_x:
                dx = constants.ENEMY_SPEED
            if self.position_y > player.position_y:
                dy = -constants.ENEMY_SPEED
            if self.position_y < player.position_y:
                dy = constants.ENEMY_SPEED
        #flip jelly image
        if dx < 0:
            self.flip = False
        if dx > 0:
            self.flip = True
        #control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)
        # Update the position
        self.position_x += 100 * delta_time * dx
        self.position_y += 100 * delta_time * dy

        if dist < constants.ATTACK_RANGE:
            self.fade_out_state = ScreenFadeOut(self.game, 0,0, self.jelly_type, CastleBattle(self.game, self.jelly_type))
            self.fade_out_state.enter_state()
            pygame.mixer.Channel(3).play(self.battle_start_sound)
         # Animate the sprite
        self.animate(delta_time, dx, dy)

    def draw(self, display):
        flipped_image = pygame.transform.flip(self.curr_image, self.flip, False)
        display.blit(flipped_image, (self.position_x, self.position_y))

    def animate(self, delta_time, dx, dy):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        #progress animation
        if self.last_frame_update > .15:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame +1) % len(self.curr_anim_list)
            self.curr_image = self.curr_anim_list[self.current_frame]

    def load_sprites(self):
        # Get the directory with the jelly sprites
        self.jelly_sprites = []
        # Load in the frames for each jelly
        temp_list = []
        for i in range(0,6):
            strawberry_sprites = pygame.image.load(f"img/Characters/jelly/strawberry/{i}.png").convert_alpha()
            strawberry_sprites = scale_image(strawberry_sprites, constants.SCALE)
            temp_list.append(strawberry_sprites)
        self.jelly_sprites.append(temp_list)
        temp_list = []
        for i in range(0,6):
            peanut_sprites = pygame.image.load(f"img/Characters/jelly/peanut/{i}.png").convert_alpha()
            peanut_sprites = scale_image(peanut_sprites, constants.SCALE)
            temp_list.append(peanut_sprites)
        self.jelly_sprites.append(temp_list)
        temp_list = []
        for i in range(0,6):
            grape_sprites = pygame.image.load(f"img/Characters/jelly/grape/{i}.png")
            grape_sprites = scale_image(grape_sprites, constants.SCALE)
            temp_list.append(grape_sprites)
        self.jelly_sprites.append(temp_list)
        temp_list = []
        for i in range(0,6):
            ancient_sprites = pygame.image.load(f"img/Characters/jelly/ancient/{i}.png")
            ancient_sprites = scale_image(ancient_sprites, constants.SCALE)
            temp_list.append(ancient_sprites)
        self.jelly_sprites.append(temp_list)
        
        # Set the default frames 
        self.curr_image = self.jelly_sprites[self.jelly_type][0]
        self.curr_anim_list = self.jelly_sprites[self.jelly_type]

#helper function to scale image
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

   
        