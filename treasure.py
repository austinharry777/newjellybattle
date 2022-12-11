import pygame 

class CastleTreasure(pygame.sprite.Sprite):
    def __init__(self, x,y, item_type, animation_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type # 0: potion, 1: Butterknife
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        

    def update(self, screen_scroll, player, treasure_fx):
        #reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        #check to see if item has been collected by player
        if self.rect.colliderect(player.player_rect):
            #treasure opened
            if self.item_type == 0:
                player.potion += 1
                treasure_fx.play()
            elif self.item_type == 1:
                pass
            self.kill()

        #handle animation
        animation_cooldown = 150
        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1 
            self.update_time = pygame.time.get_ticks()
        #check if animation has finished
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self, display):
        display.blit(self.image, self.rect)
