import pygame
import constants 
import math 

class Player():
    def __init__(self,game, x,y):
        self.game = game
        self.load_sprites()
        self.position_x, self.position_y = (x,y)
        self.player_rect = self.curr_image.get_rect()
        self.current_frame, self.last_frame_update = 0,0
        
        
    def update(self, delta_time, actions, obstacle_tiles):
        #camera variable
        screen_scroll = [0,0]
        dx = actions["right"] - actions["left"]
        dy = actions["down"] - actions["up"]
        #control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        # Update the position
        if actions['action1']:
            self.position_x += 250 * delta_time * dx
            for obstacle in obstacle_tiles:
                #check for collision
                if obstacle[1].collidepoint(self.position_x + 48, self.position_y + 24):
                    #check which side the collision is from
                    if dx > 0:
                        self.position_x = obstacle[1].left - 48
                if obstacle[1].collidepoint(self.position_x, self.position_y + 24):    
                    if dx < 0:
                        self.position_x = obstacle[1].right
            
            self.position_y += 250 * delta_time * dy
            for obstacle in obstacle_tiles:
                #check for collision
                if obstacle[1].collidepoint(self.position_x + 24, self.position_y + 48):
                    #check which side the collision is from
                    if dy > 0:
                        self.position_y = obstacle[1].top - 48
                if obstacle[1].collidepoint(self.position_x + 24, self.position_y):
                    if dy < 0:
                        self.position_y = obstacle[1].bottom
        else:
            self.position_x += 150 * delta_time * dx
            for obstacle in obstacle_tiles:
                #check for collision
                if obstacle[1].collidepoint(self.position_x + 48, self.position_y + 24):
                    #check which side the collision is from
                    if dx > 0:
                        self.position_x = obstacle[1].left - 48
                if obstacle[1].collidepoint(self.position_x, self.position_y + 24):
                    if dx < 0:
                        self.position_x = obstacle[1].right

            self.position_y += 150 * delta_time * dy
            for obstacle in obstacle_tiles:
                #check for collision
                if obstacle[1].collidepoint(self.position_x + 24, self.position_y + 48):
                    #check which side the collision is from
                    if dy > 0:
                        self.position_y = obstacle[1].top - 48
                if obstacle[1].collidepoint(self.position_x + 24, self.position_y):
                    if dy < 0:
                        self.position_y = obstacle[1].bottom
        #update scroll based on player position
        #move camera left and right
        if self.position_x > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
            screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.position_x
            self.position_x = constants.SCREEN_WIDTH - constants.SCROLL_THRESH
        if self.position_x < constants.SCROLL_THRESH:
            screen_scroll[0] = constants.SCROLL_THRESH - self.position_x
            self.position_x = constants.SCROLL_THRESH

        #move camera up and down
        if self.position_y > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
            screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.position_y
            self.position_y = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
        if self.position_y < constants.SCROLL_THRESH:
            screen_scroll[1] = constants.SCROLL_THRESH - self.position_y
            self.position_y = constants.SCROLL_THRESH
        
        # Animate the sprite
        self.animate(delta_time, dx, dy)

        return screen_scroll

    def draw(self, display):
        display.blit(self.curr_image,(self.position_x, self.position_y))
        #pygame.draw.rect(display, constants.RED, self.player_rect, 1)

    def animate(self, delta_time, dx, dy):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # If no direction is pressed, set image to idle and return
        if not (dx or dy): 
            self.curr_image = self.curr_anim_list[0]
            return
        # If an image was pressed, use the appropriate list of frames according to direction
        if dx:
            if dx > 0: self.curr_anim_list = self.right_sprites
            else: self.curr_anim_list = self.left_sprites
        if dy:
            if dy > 0: self.curr_anim_list = self.front_sprites
            else: self.curr_anim_list = self.back_sprites
        # Advance the animation if enough time has elapsed
        if self.last_frame_update > .15:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame +1) % len(self.curr_anim_list)
            self.curr_image = self.curr_anim_list[self.current_frame]

    def load_sprites(self):
        #orthogonal sprites
        # Get the directory with the player sprites
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [],[],[],[]
        # Load in the frames for each direction
        for i in range(0,4):
            front_sprites = pygame.image.load(f"img/Characters/hero/femtatfront/{i}.png").convert_alpha()
            front_sprites = scale_image(front_sprites, constants.SCALE)
            self.front_sprites.append(front_sprites)
            back_sprites = pygame.image.load(f"img/Characters/hero/femtatback/{i}.png").convert_alpha()
            back_sprites = scale_image(back_sprites, constants.SCALE)
            self.back_sprites.append(back_sprites)
            right_sprites = pygame.image.load(f"img/Characters/hero/femtatright/{i}.png").convert_alpha()
            right_sprites = scale_image(right_sprites, constants.SCALE)
            self.right_sprites.append(right_sprites)
            left_sprites = pygame.image.load(f"img/Characters/hero/femtatleft/{i}.png").convert_alpha()
            left_sprites = scale_image(left_sprites, constants.SCALE)
            self.left_sprites.append(left_sprites)
        
        # Set the default frame to stand still
        self.curr_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites

#helper function to scale image
def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))